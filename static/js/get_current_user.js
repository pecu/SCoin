function get_current_user(url) {
    $.ajax({
        url: url,
        type: 'get',
        async: true,
        success: function (res) {
		document.getElementById('sender').innerHTML = res;
		console.log(res);
                return true;
        },
        error: function (res) {
            return false;
        }
    });
}
