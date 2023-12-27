function openModal(text) {
     //console.log(text);
    document.getElementById('modalText').innerHTML = text;
    document.getElementById('myModal').style.display = 'block';
  }  function closeModal(text) {
    document.getElementById('myModal').style.display = 'none';
  }
        // Your JavaScript code here
        if (message !== "") {
            //console.log(message);
            //message.replace("</br>",'\n');
            //var modalElement = document.getElementById('your-modal-id');

                openModal(message);
        } else {
            console.log("not yes");
        }