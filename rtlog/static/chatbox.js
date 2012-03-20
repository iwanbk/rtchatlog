var ChatBox = function(options)
{
    var _this = this;
    _this.pollUrl = options.pollUrl;
    _this.newMessageUrl = options.newMessageUrl;
    $('#messageform').submit(function() { _this.newMessage(); return false; });
    _this.poll();
}

ChatBox.prototype.showMessages = function(response)
{
    var _this = this;
    if (response){
        html = []
        for (var i=0; i < response.messages.length; i++){
            html.push('<li>' + response.messages[i] + '</li>');
        }
        $('#messages').html(html.join(""));
    }
}

ChatBox.prototype.poll = function()
{
    var _this = this;
   
    var callback = function(response)
    {
        _this.showMessages(response);
        setTimeout(function(){  _this.poll(); }, 0);
    }

    $.post(_this.pollUrl, null, callback, "json");
}

ChatBox.prototype.newMessage = function(message)
{
    var _this = this;

    if (!message){
        message = $('#message').val();
    } 

    var callback = function(response)
    {
        $('#message').val('');
    }
    
    if (message){
        var params = { body : message };
        $.post(_this.newMessageUrl, params, callback, "json");
    } 
}
