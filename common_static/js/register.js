function SignUp(){
	var User_id=$("#SignUp_UserName").val();
	var Pwd=$("#SignUp_Pwd").val();
	if(User_id=="" ||Pwd==""){
		alert('Please Input user name and password!');
		return;
	}		
	$.ajax({
	type:"POST",
	url:"SignUp/",
	data:{'User_id1':User_id,'Pwd1':Pwd},
	success:function (result) {
				var returned_data=jQuery.parseJSON(JSON.stringify(result));
				$('#SignUp_result').html('');
				$('#SignUp_result').append("<h4>"+returned_data+"</h4><br/>");
				
			},
	error:function (result) {
			 console.log("something wrong with returned_data");
		  }
	});
	
};
