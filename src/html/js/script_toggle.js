(function() {

$(function() {
	// スマホ用メニューボックスの開閉
	$("#toggle").click(function() {
		$("#menu").slideToggle();
		return false;
	});
	$(window).resize(function() {
//		var win = $(window).width();
//		var p = 640;
//		if(win > p) {
//			$("#menu").show();
//		} else {
			$("#menu").hide();
//		}
	});
	$("#menu li a").click(function() {
		$("#menu").slideToggle();
//		return false;
	});
});

// SPで位置調整
// $(function() {
// $(window).load(function () {
// jQuery 3.xからこれでないと動かない
$(window).on('load', function() {
	SetBoxDummy();
});

$(function() {
	$(window).on('resize', function() {
		SetBoxDummy();
	});
});


function SetBoxDummy() {
	var height = document.getElementById("menuBox").clientHeight;
	// alert(height);
	$('#menuBoxDummy').css('height', height+"px");
}

})();

