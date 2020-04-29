function get_balance_by_user(url) {
    $.ajax({
        url: url,
        type: 'get',
        async: true,
        success: function (res) {
		list_balance = res.split("\n");
		balance = 0;
		if (res != "" && list_balance.length > 0)
			balance = list_balance.length;
		else
			balance = 0
  		
		document.getElementById('balance').innerHTML = "Balance: " + balance.toString();
                return true;
        },
        error: function (res) {
            return false;
        }
    });
}
