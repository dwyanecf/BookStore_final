function SignIn(){
	var User_id=$("#SignIn_UserName").val();
	var Pwd=$("#SignIn_Pwd").val();
	console.log(User_id);
	if(User_id=="" ||Pwd==""){
		alert('Please Input user name and password!');
		return;
	}		
	$.ajax({
	type:"POST",
	url:"SignIn/",
	data:{'User_id':User_id,'Pwd':Pwd},
	success:function (result) {
				var returned_data=jQuery.parseJSON(JSON.stringify(result));
				$('#SignIn_result').html('');
				$('#SignIn_result').append("<h4>"+returned_data+"</h4><br/>");
				
			},
	error:function (result) {
			 console.log("something wrong with returned_data");
		  }
	});
	
};
