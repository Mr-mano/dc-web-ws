$(function () {
	socket = io.connect('http://' + document.domain + ':' + location.port);
	socket.on('connect', function() {
		$('#status').html('Connecté');
    	socket.emit('client_connected', {data: 'New client!'});
	});

	socket.on('disconnect', function() {
		$('#status').html('Déconnecté');
	});

	socket.on('alert', function (data) {
    	$('#status').html('Connecté');
        $('#content').html(data + "<br />");
	});

        socket.on('loop', function (data) {
        $('#content').html(data + "<br />");
        });

});
