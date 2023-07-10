document.addEventListener('DOMContentLoaded', () => {
	//To connect to socketio server
	var socket=io.connect('http://' + document.domain + ':' + location.port);
	let room;
	//when sending data from server to event bucket
	socket.on('message', data => {
		const p=document.createElement('p');
		const br=document.createElement('br');
		const span_usrname=document.createElement('span');
		const span_time=document.createElement('span');
		span_time.innerHTML=data.time_stamp;
		span_usrname.innerHTML=data.username;
		p.innerHTML=span_usrname.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time.outerHTML;
		document.querySelector('#display-message-section').append(p); 
	});
	
	document.querySelector('#send_message').onclick = () =>{
		socket.send({'msg': document.querySelector('#user_message').value,'username':username, 'room':room });
	}

	document.querySelectorAll('.select-room').forEach(p => {
		p.onclick = () => {
			let newroom=p.innerHTML;
			if (newroom==room){
				msg=`You are already in ${room} room`;
				printSysMsg(msg);
			}
			else{
				leaveRoom(room);
				joinRoom(newroom);
				room=newroom;
			}
		}
	});

	function leaveRoom(room){
		socket.emit('leave', {'username':username, 'room':room});
	}

	function joinRoom(room){
		socket.emit('join', {'username':username, 'room':room});
		document.querySelector('#display-message-section').innerHTML='';
	}

	function printSysMsg(msg){
		const p=document.createElement('p');
		p.innerHTML=msg;
		document.querySelector('#display-message-section').append(p);
	}
})