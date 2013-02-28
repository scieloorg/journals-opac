bots = ['bot', 'link', 'web', 'lib', 'yahoo'];

function is_bot(agent) {
    for (var bot in bots) {
        var botina = bots[bot];
        if (agent.indexOf(botina) != -1) {
            return true;
        }
    }
    return false;
}

function send_access(ratchet_obj) {
    var url = ratchet_obj.ratchet_uri + ratchet_obj.resource;

    delete ratchet_obj.ratchet_uri;
    delete ratchet_obj.resource;

    if (is_bot(navigator.userAgent) === false){
        $.post(url, ratchet_obj, function (data) { return true; });
    }
}