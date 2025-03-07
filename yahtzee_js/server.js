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

  socket.on('game_connection', function(data) {  
    socket.join(data.game_name);
    console.log('Socket game connection event:', data.username, io.sockets.adapter.rooms.get(data.game_name).size);

    io.to(data.game_name).emit('game_connection', {
        username:data.username,
        num_game_connections: io.sockets.adapter.rooms.get(data.game_name).size
    });
  }); 

  socket.on('chat', function(data) {
    console.log('Socket chat event:', data);
    io.to(data.game_name).emit('chat', {
      username: data.username,
      message: data.message
    });
  });


 
});
// app.get('/games/:game_name/:data'), async function(request)

// this process circumvents the need for controllers. we write the function that the controller would run right here.
app.get('/games/:game_name/:username', async function(request, response) { // front end pings this to get the page.  need to put fetch here  bc you need to send . change links to the node server on user_games
  let username = request.params.username;
  let game_name = request.params.game_name;
  console.log("username is", username)
  console.log(`game name is ${game_name}`)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("index", {
    username: username,
    game_name: game_name
  });
});

//start the server. node server is the only one that renders the actual yahtzee game.
const port = process.env.PORT || 3000;
app.set('port', port); //let heroku pick the port if needed

server.listen(port, function() {
  console.log('Server started at http://localhost:'+port+'.')
});
