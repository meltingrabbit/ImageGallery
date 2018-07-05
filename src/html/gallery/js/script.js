(function() {

// とりあえずDOM構築が終わったら整形
$(function() {
	SetImgHeight();
	GetImageArea();
});
// $(function() {		// こっちだとスクロールバーができる前にwidthを取得してしまう
// さらに画像読み込みが終了し，スクロールバーなどができ画面幅が小さくなったら再整形
// $(window).load(function () {
// jQuery 3.xからこれでないと動かない
$(window).on('load', function() {
	SetImgHeight();
	FitImgHeight();
	$(window).on('resize', function() {
		console.log('resize!!');
		SetImgHeight();
		FitImgHeight();
	});
});



// クリックイベント登録
$(function() {
	var maxPageNum = $("#maxPageNum").text();
	// alert(maxPageNum);

	$("select[name='type']").change(function() {
		$('input[name="page"]').val(1);
		$("#goButton").click();
	});

	$("#goButton").on("click", function() {
		// alert("GO!");
		EmptyImageArea();
		GetImageArea();
	});
	$("#changeButton").on("click", function() {
		// alert("Change!");
		ChangeSeed();
		EmptyImageArea();
		GetImageArea();
	});

	$(".page-up").on("click", function() {
		// alert("Up");
		var page = $('input[name="page"]').val();
		page++;
		if (page > maxPageNum) {
			page = maxPageNum;
		}
		$('input[name="page"]').val(page);
		$("#goButton").click();
	});
	$(".page-down").on("click", function() {
		// alert("Down");
		var page = $('input[name="page"]').val();
		page--;
		if (page < 1) {
			page = 1;
		}
		$('input[name="page"]').val(page);
		$("#goButton").click();
	});

});

// 通信関連
$(function() {
	$(document).ajaxError(function(e, xhr, opts, error) {
		alert('サーバー内部でエラーが発生しました．');
		// alert('AjaxError：' + error+', '+e+', '+xhr+', '+opts);
	});
});

// ##################################
// 関数

// 高さをそろえる関数
function SetImgHeight() {
	console.log("SIH");
	var width = document.getElementById("imageArea").clientWidth -0;
	var col = 0.0;
	if (width >= 1300) {
		col = 4.0;
	} else if (width >= 640) {
		col = 3.0;
	} else {
		col = 2.0;
	}
	var imgHeight = width / 3.0 * 2.0 / col;
	// console.log(width+":"+imgHeight);
	// $('#imageArea img.photo').css('height', imgHeight+"px");
	$('img.photo').css('height', imgHeight+"px");
	var padding = width * 0.2 / 100.0;
	// var padding = width * 1 / 100.0;
	var paddingH = width * 2 / 100.0;
	var paddingV = imgHeight * 5 / 100.0;
	$('img.photo').css('padding', padding+"px");
	$('#imageArea .photo_container .description').css('padding-top', paddingV+"px");
	$('#imageArea .photo_container .description').css('padding-bottom', paddingV+"px");
	$('#imageArea .photo_container .description').css('padding-left', paddingH+"px");
	$('#imageArea .photo_container .description').css('padding-right', paddingH+"px");
	$('#imageArea .photo_container img.X').css('top', paddingH+"px");
	$('#imageArea .photo_container img.X').css('right', paddingH+"px");
	$('div.imgDummy').css('margin', padding+"px");
}


// 隙間がある行の高さを延ばす関数
// 最初，同じ行のを配列に集めてその都度リサイズしていたが，リサイズ途中にoffsetがかわっておかしくなったので，
// まず，同じ行の配列を要素に持つ二次元配列を作成した．その後，まとめてリサイズ．
function FitImgHeight() {
	var imgNum = $('div.photo_container').length;
	var width = document.getElementById("imageArea").clientWidth;
	var div2dArr = [];
	var divArr = [];
	var top    = -100;
	var preTop = -100;
	// console.log(width);
	// console.log(imgNum);

	// 要素がない場合，抜ける
	if (imgNum == 0) {
		return false;
	}

	// 同じ行の要素を配列に集める
	top = $('div.photo_container').eq(0).offset().top;
	divArr.push(0);
	for(var i=1; i<imgNum ;i++) {
		// console.log($('div.photo_container').eq(i).find('p').eq(0).text());
		// console.log($('div.photo_container').eq(i).outerWidth(true));
		// console.log($('div.photo_container').eq(i).offset().top);

		preTop = top;
		top = $('div.photo_container').eq(i).offset().top;
		if (top == preTop) {
		} else {
			div2dArr.push(divArr);
			divArr = [];
		}
		divArr.push(i);
	}
	div2dArr.push(divArr);
	// console.log(div2dArr);


	// リサイズ
	// とりあえず1引いとく（安全策）
	width = document.getElementById("imageArea").clientWidth * 0.99;
	// width = document.getElementById("imageArea").clientWidth;
	for(var i=0,l=div2dArr.length; i<l; i++) {
		var widthSum = 0;
		// var height = $('div.photo_container').eq(div2dArr[i][0]).outerHeight(true);
		var height = $('div.photo_container').eq(div2dArr[i][0]).find('img.photo').outerHeight(true);
		// console.log(div2dArr[i]);
		for(var j=0,m=div2dArr[i].length; j<m; j++) {
			// console.log(div2dArr[i][j]);
			widthSum += $('div.photo_container').eq(div2dArr[i][j]).outerWidth(true) + 0;
		}

		var scale = width / widthSum;

		// console.log(width);
		// console.log(widthSum);
		// console.log(scale);
		// console.log(height);
		// console.log(height*scale);

		for(var j=0,m=div2dArr[i].length; j<m; j++) {
			// console.log(div2dArr[i][j]+" : "+(height*scale));
			// $('div.photo_container').eq(div2dArr[i][j]).css('height', (height*scale)+"px");
			// $('div.photo_container').eq(div2dArr[i][j]).css('height', (300)+"px");
			// $('div.photo_container').eq(div2dArr[i][j]).find('img.photo').css('height', 400+"px");
			$('div.photo_container').eq(div2dArr[i][j]).find('img.photo').css('height', (height*scale)+"px");
			// $('div.photo_container').eq(div2dArr[i][j]).find('img.photo').css('height', (height*0.5)+"px");
			// console.log(height*scale);
		}
	}
}

function EmptyImageArea() {
	$("#imageArea").empty();
}

function ChangeSeed() {
	var seed = Math.floor( Math.random() * 100000 );
	$("#seed").text(seed);
}

function GetImageArea() {
		$.post('./cgi/getImageArea.cgi',
			{
				// no : '2017033001',
				// name : $('input').val(),
				// cmnt : $('textarea').val(),
				IMG_NUM : $('input[name="IMG_NUM"]').val(),
				type : $('select[name="type"]').val(),
				page : $('input[name="page"]').val(),
				seed : $('#seed').text(),
				end : 'end'
			},
			function(data) {
				// console.log(data);
				if (data == -1) {
					alert('サーバー内部でエラーが発生しました．');
				} else {
					// $("#imageArea").append(data);
					// // data.ready(function() {
					// // data.on('load', function() {
					// $("#imageArea").on('load', function() {
					// 	console.log("load");
					// 	SetImgHeight();
					// 	FitImgHeight();
					// });

					// ↑だと，imgのloadが終わる前に画像サイズなどを取得しようとし，SetImgHeight()などが正常に動かない

					// $("#imageArea").append(data);
					// jQuery Objectへ変換
					var $data = $(data);
					console.log($data);
					$("#imageArea").append($data);
					// $data.ready(function() {

					// console.log("ready");
					SetImgHeight();
					var count = 0;
					// var imgNum = $('div.photo_container').length * 2;	// div1つにつきimg2個
					$("#imageArea").find("img.photo").on("load",function() {
						// var imgNum = $('div.photo_container').length * 2;	// div1つにつきimg2個
						var imgNum = $('div.photo_container').length;
						console.log("load");
						// SetImgHeight();
						// FitImgHeight();
						count++;
						// console.log(count);
						// console.log(imgNum);
						// if (count == imgNum) {
						if (count == imgNum || count == Math.floor(imgNum/2.0)) {
							SetImgHeight();
							FitImgHeight();

		// 					// lightbox再読込
		// 					// これで一応動くけど..... ぐるぐるとかの挙動がおかしい．


  // new Lightbox({
  //   loadingimg:'/etc/lightbox/resource/loading.gif',
  //   expandimg:'/etc/lightbox/resource/expand.gif',
  //   shrinkimg:'/etc/lightbox/resource/shrink.gif',
  //   blankimg:'/etc/lightbox/resource/blank.gif',
  //   previmg:'/etc/lightbox/resource/prev.gif',
  //   nextimg:'/etc/lightbox/resource/next.gif',
  //   closeimg:'/etc/lightbox/resource/close.gif',
  //   effectimg:'/etc/lightbox/resource/zzoop.gif',
  //   effectpos:{x:-40,y:-20},
  //   effectclass:'effectable',
  //   resizable:true,
  //   animation:true
  // });



						}
					});

					// });



					// $data.ready(function() {
					// $data.load(function() {
					// $data.on("load",function() {
					// $("#imageArea").on("load",function() {
					// $("#imageArea").find("div").on("load",function() {
					// $("#testhoge").on("load",function() {
					// $("#imageArea").find("#testhoge").on("load",function() {
					// $(window).on("load",function() {

	// // tbody.mainから指定しているのは、後から動的に出来たボタンにも対応するため
	// $('tbody.main').on('click', 'button.copy2nxtwk', function() {

					// $("#imageArea").on("load", 'img', function() {

					// var count = 0;
					// var imgNum = $('input[name="IMG_NUM"]').val();

					// $("#imageArea").find("img").on("load",function() {
						// SetImgHeight();
						// FitImgHeight();
						// console.log("load");
						// count++;
						// console.log(count);
						// console.log(imgNum);
					// });
					// $("#imageArea").append($data);
					// console.log("llll");
					// $data.on('load', function() {
					// // $data.ready(function() {		// これじゃあDOM構築のみでloadは終わってない．
					// 	console.log("load");
					// 	SetImgHeight();
					// 	FitImgHeight();
					// });
				}
				return false;
			}
		);
}



// Magnific Popup

$(function(){
// $('.parent-container').magnificPopup({
$('#imageArea').magnificPopup({
	delegate: 'a',
	type: 'image',
	gallery: { //ギャラリー表示にする
		enabled:true,
		preload: [0,1],
		navigateByImgClick: true,
	}
	});
});


})();
