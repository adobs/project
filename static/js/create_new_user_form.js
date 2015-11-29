  function printStatus(results){
        console.log("made it to print status");
        $("#loading").hide();
        if (results==="This email is already in use."){
            $('#email-status').html(results);
        }
        else if (results==="Screenname already in use."){
            $('#screenname-status').html(results);
        }
        else if (results === "Password is too weak, choose again."){
            $('#password-status').html(results);
        }
        else if (results === "success") {
            $('#new-user-form').unbind("submit");
            $('#new-user-form').submit();
        }
    
        $('#submit-btn').removeAttr('disabled');
    }

    function checkStatus(){
    //could this all be done with form "sterilization"?  form.sterilze

        var formInputs = {
            "orientation": $(".orientation").val(),
            "gender": $(".gender").val(),
            "birthmonth": $("#birthmonth").val(),
            "birthdate": $("#birthdate").val(),
            "birthyear": $("#birthyear").val(),
            "zip": $("#zip").val(),
            "email": $("#email").val(),
            "screenname": $("#screenname").val(),
            "password": $("#password").val()
        };


        $.post('/new-user', formInputs, printStatus);
        console.log("made it to check status")
    }

    function submitForm(evt){
        evt.preventDefault();
        $('#loading').show();
        console.log("hey");
        $('#email-status').html("");
        $('#screenname-status').html("");
        $('#password-status').html("");

        $('#submit-btn').attr('disabled',true);
        checkStatus();
    }
        
    $('#loading').hide();
    $('#new-user-form').on("submit", submitForm);
