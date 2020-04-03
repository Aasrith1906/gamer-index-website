

var key = "kiawougd"

var socket = io.connect('http://' + document.domain + ':' + location.port + '/Chat');

        $('#logout').click(function()
        {
            location.href = 'http://' + document.domain + ':' + location.port + '/logout';
        });

        socket.on('UserConnectionResponse',function(message)
        {
            console.log(message);
            $('div.message-holder').append('<div><b>'+message['username']+'</b> '+message['data']+'</div>' )
        })

        socket.on('RecieveUserMessage',
        function(message){
            var message_value_decrypted = CryptoJS.AES.decrypt(message.data,key).toString(CryptoJS.enc.Utf8)
            $('div.message-holder').append('<div><b>' +message['username'] +'</b> '+ ':' + message_value_decrypted.toString() +'</div>' )

        })


        $('form.form').submit(
            function(e)
            {
                e.preventDefault()
                var message = $('#EnterMessage').val();
                var message_encrypted = CryptoJS.AES.encrypt(message , key)
                console.log(message_encrypted.toString())
                document.getElementById('EnterMessage').value = null
                socket.emit('UserMessage' , message_encrypted.toString());
               
            }
        )

       