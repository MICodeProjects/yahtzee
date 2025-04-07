const fetch=require('node-fetch')
let express = require('express');
let app = express();

//Socket Conection
let server = require('http').Server(app);
let io = require('socket.io')(server);

//Middleware
const ejs = require('ejs');
const { ok } = require('assert');
app.use(express.static('public')); //specify location of static assests
app.set('views', __dirname + '/views'); //specify location of templates
app.set('view engine', 'ejs'); //specify templating library

io.on('connection', function(socket){  
  console.log("io is on")
  io.emit('connection', {
    num_total_connections: io.engine.clientsCount
  }); 

  socket.on("ui.js_game_connection", async function(data){
    socket.join(data.game_name)
  })
  socket.on("game_connection", async function(data){
    socket.join(data.game_name)
    game_name = data.game_name
    username = data.username
    const link = `http://127.0.0.1:8080/scorecards/game_connection_data/${data.game_name}/${username}`
    // fetch data
      try {
        const response = await fetch(link);
        // const response = await fetch(link, {method:"POST", headers:{"usergamename":request_header}});
        console.log(response)
        
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        // getting data from fetch and the status
        const json = await response.json()

          
          // emit game_connection data to all clients
          io.to(data.game_name).emit('game_connection', { // what it emits at the game connection to all the clients.
            username: username,
            game_name: game_name,
            players:JSON.stringify(json.players),
            scorecards:JSON.stringify(json.scorecards),
            turn_order:JSON.stringify(json.turn_order),
            num_game_connections: io.sockets.adapter.rooms.get(data.game_name).size

          });
  
      } catch (error) {
          console.error(error.message);
      }
    
    console.log("socket.on game connection is running")
      
  
  });

  socket.on('chat', function(data) {
    console.log('Socket chat event:', data);
    io.to(data.game_name).emit('chat', {
      username: data.username,
      message: data.message
    });
  });

  socket.on("die_reserved", function(data){
    io.to(data.game_name).emit("die_reserved", {
      "die_position":data.die_position,
      "username":data.username
    })
  })

  // remember: client emits, then server recieves w/ socket.on, then emits to clients w/ io.to
  socket.on('valid_score', async function(data) {
    console.log('Socket valid_score event:', data);
    // update DB
    const link = `http://127.0.0.1:8080/scorecards/scorecards_update`
    
    const response = await fetch(link, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ categories: data.categories, scorecard_name:data.scorecard_name, game_name:game_name})
    });

    if (!response.ok){
      throw new Error(`Response status: ${response.status}`);
    }

      // Emit the valid score event to all players
      io.to(data.game_name).emit('valid_score', {
          username: data.username,
          scorecard: data.categories
      });
      console.log("Server emitted valid score event")
  });
  
  // when dice are rolled
  socket.on("dice_rolled", function(data){
    io.to(data.game_name).emit('dice_rolled', {
      dice_values:data.dice_values,
      rolls_remaining:data.rolls_remaining
    })
    console.log("Server emitted dice_rolled event")

  })

});



// this process circumvents the need for controllers. we write the function that the controller would run right here.
app.get('/games/:game_name/:username', async function(request, response) { // front end pings this to get the page.  need to put fetch here  bc you need to send . change links to the node server on user_games
  let username = request.params.username;
  let game_name = request.params.game_name;

  const link = `http://127.0.0.1:8080/scorecards/game_connection_data/${game_name}/${username}`
  try {
    const response1 = await fetch(link);
    if (!response1.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    // getting data from fetch and the status
    const json = await response1.json()
    console.log(`Json players: ${JSON.stringify(json.players)}`)

    // Render the EJS template with the data
    response.status(200);
    response.setHeader('Content-Type', 'text/html');
    response.render("index", {
      username: username,
      game_name: game_name,
      players: json.players,
      turn_order:json.turn_order
  });
  } catch (error) {
    console.error(error.message);
    response.status(500).send("An error occurred while fetching data.");
  }
});

//start the server. node server is the only one that renders the actual yahtzee game.
const port = process.env.PORT || 3000;
app.set('port', port); //let heroku pick the port if needed

server.listen(port, function() {
  console.log('Server started at http://localhost:'+port+'.')
});
