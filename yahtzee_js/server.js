let express = require('express');
let app = express();

//Socket Conection
let server = require('http').Server(app);
let io = require('socket.io')(server);

//Middleware
const ejs = require('ejs');
app.use(express.static('public')); //specify location of static assests
app.set('views', __dirname + '/views'); //specify location of templates
app.set('view engine', 'ejs'); //specify templating library

io.on('connection', function(socket){  
  console.log("io is on")
  io.emit('connection', {
    num_total_connections: io.engine.clientsCount
  }); 

  socket.on("game_connection", async function(data){
    socket.join(data.game_name)
    const request_header = [data.username, data.game_name]
    const link = `http://127.0.0.1:8080/scorecards/game_connection_data/${data.game_name}`
    // fetch data
      try {
        const response = await fetch(link); //const response = await fetch(players_link, {method:"POST", headers:{"usergamename":requestheader}});
        
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        // getting data from fetch and the status
        const json = await response.json()


          const players = json.players
          const scorecards = json.scorecards
          
          // emit game_connection data to all clients
          io.to(data.game_name).emit('game_connection', { // what it emits at the game connection to all the clients.
            username: data.username,
            game_name: data.game_name,
            players:players,
            scorecards:scorecards,
            num_game_connections: io.sockets.adapter.rooms.get(data.game_name).size

          });
        
  
      } catch (error) {
          console.error(error.message);
      }

      
  
  });

  socket.on('chat', function(data) {
    console.log('Socket chat event:', data);
    io.to(data.game_name).emit('chat', {
      username: data.username,
      message: data.message
    });
  });


 
});




// this process circumvents the need for controllers. we write the function that the controller would run right here.
app.get('/games/:game_name/:username', async function(request, response) { // front end pings this to get the page.  need to put fetch here  bc you need to send . change links to the node server on user_games
  let username = request.params.username;
  let game_name = request.params.game_name;

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("index", {
    username: username,
    game_name: game_name,
  });
});

//start the server. node server is the only one that renders the actual yahtzee game.
const port = process.env.PORT || 3000;
app.set('port', port); //let heroku pick the port if needed

server.listen(port, function() {
  console.log('Server started at http://localhost:'+port+'.')
});
