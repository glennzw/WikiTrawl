<html>
<head>
<script type="text/javascript" src="libs/jquery-1.7.2.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
 $("button").attr("disabled", false);
  $("button").click(function(){
	$("button").attr("disabled", true);
	$("button").html("Working...");
	$("p").empty();

	var first = $("#start_term").val();
	var curr = first;
	$("p").append("<br><a href='http://en.wikipedia.org/wiki/"+curr+"'>" + curr + "</a> links to:");

	while( curr != "Philosophy"){

		$.ajax({
		  url: "getNext.php?term=" + curr,
		  async: false,
		  //dataType: 'json',
		  cache: false

		}).done(function( html ) {

		var obj = jQuery.parseJSON(html);
		prev=curr;
		curr=obj.result;
		if( curr != "Philosophy"){
			$("p").append("<br><a href='http://en.wikipedia.org/wiki/"+curr+"'>" + curr + "</a> links to:");
		}
		else{
			$("p").append("<br><a href='http://en.wikipedia.org/wiki/"+curr+"'>" + curr + "</a>");
		}


		});

	}
	$("p").append("<p>")
	$("button").attr("disabled", false);
	$("button").html("Click me")



  });
});
</script>
</head>

<body>
<h2>WikiTrawl - Everything leads to Philosophy</h2>
<input Value="Sheep" type="text" id="start_term">
<br>


<button>Click me</button>
<p></p>
</body>
</html>
