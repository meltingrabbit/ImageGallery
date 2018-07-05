

// とりあえずDOM構築が終わったら整形
$(function() {
	SetImgHeight();
});
// $(function() {		// こっちだとスクロールバーができる前にwidthを取得してしまう
// さらに画像読み込みが終了し，スクロールバーなどができ画面幅が小さくなったら再整形
$(window).load(function () {
	SetImgHeight();
	FitImgHeight();
	$(window).on('resize', function() {
		console.log('resize!!');
		SetImgHeight();
		FitImgHeight();
	});
});


// 高さをそろえる関数
function SetImgHeight() {
	var width = document.getElementById("imageArea").clientWidth;
	var col = 0.0;
	if (width >= 1300) {
		col = 4.0;
	} else if (width >= 640) {
		col = 3.0;
	} else {
		col = 2.0;
	}
	var imgHeight = width / 3.0 * 2.0 / col;
	console.log(width+":"+imgHeight);
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
	var divArr = [];
	var top    = -100;
	var preTop = -100;
	console.log(width);
	// console.log(imgNum);

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
			RecalcImgHeight(divArr);
			divArr = [];
		}
		divArr.push(i);
	}
	RecalcImgHeight(divArr);
}

function RecalcImgHeight(divArr) {
	console.log(divArr);

	// if (divArr[0] != 3 && divArr[0] != 0) {
	if (divArr[0] != 0) {
		return false;
	}

	// とりあえず1引いとく（安全策）
	var width = document.getElementById("imageArea").clientWidth -10;
	var widthSum = 0;
	var height = $('div.photo_container').eq(divArr[0]).outerHeight(true);
	// var height = $('div.photo_container').eq(divArr[0]).find('img.photo').outerHeight(true);
	for(var i=0,l=divArr.length; i<l; i++) {
		// console.log(divArr[i]);
		widthSum += $('div.photo_container').eq(divArr[i]).outerWidth(true);
	}

	var scale = width / widthSum;

	// console.log(width);
	// console.log(widthSum);
	// console.log(scale);
	// console.log(height);
	// console.log(height*scale);

	for(var i=0,l=divArr.length; i<l; i++) {
		console.log(divArr[i]+" : "+(height*scale));
		// $('div.photo_container').eq(divArr[i]).css('height', (height*scale)+"px");
		// $('div.photo_container').eq(divArr[i]).css('height', (300)+"px");
		// $('div.photo_container').eq(divArr[i]).find('img.photo').css('height', 400+"px");
		$('div.photo_container').eq(divArr[i]).find('img.photo').css('height', (height*scale)+"px");
		// $('div.photo_container').eq(divArr[i]).find('img.photo').css('height', (height*0.5)+"px");
		// console.log(height*scale);
	}

}


