function sendmessage(){
    const input=document.getElementById("userinput");
    const chatbox=document.getElementById("chatbox");
    const usertext=input.ariaValueMax.trim();
    if(usertext==" ")
        return;
    const usermessage=`<p><strong>YOU:<strong> ${usertext}<p>`;
    chatbox.innerHTML+=usermessage;
    const botreply=`<p><strong>AI:<strong> Hello! you said "${usertext}"<p>`;
    chatbox.innerHTML+=botreply;
    input.value=" ";    //clear input box
}