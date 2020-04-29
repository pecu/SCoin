function generate_table(list_balance) {
    var table = document.getElementById("token_table"); 

    for (index = 0; index < list_balance.length; index ++) {
        var row = table.insertRow(0);
        row.innerHTML = "<a href='"+ "https://thetangle.org/transaction/" + list_balance[index] +"'>" +　
            list_balance[index].substr(1, 15) + " ..." + " </a>" ;
    }

}

function get_all_tokens_by_user(url) {
    $.ajax({
        url: url,
        type: 'get',
        async: true,
        success: function (res) {
		list_balance = res.split("\n");
		generate_table(list_balance);
                return true;
        },
        error: function (res) {
            return false;
        }
    });
}
