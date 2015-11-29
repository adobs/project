  function printStatus(results){
        if(results==="True"){
            $('#login-form').unbind('submit');
            $('#login-form').submit();
             console.log(results);
        }else{
            $("#login-status").html("Invalid username/password.").attr("class","alert alert-danger").attr("role", "alert")
        }
    }

    function verifyLogin(evt){
        evt.preventDefault();

        var formInputs = {
            "screenname": $("#screenname").val(),
            "password": $("#password").val()
        };
        
        $.post('/login', formInputs, printStatus);

    }

    $("#login-form").on('submit', verifyLogin);


