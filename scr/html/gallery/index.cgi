#!/usr/bin/perl

use strict;
use warnings;
use utf8;
binmode STDOUT, ':utf8';
#use Time::Local;

#use utf8;
#use Encode qw(decode_utf8 encode_utf8);
# perlの文字化け問題、まじで謎...
# こういう論理的な知識を体系的に身に付けるには、ラクダ本読まないとダメなのかな...？
# http://tech.voyagegroup.com/archives/465806.html


my $DIR = "../";
my $PAGE = "gallery/index.cgi";

my $PL_DIR = $DIR.'../etc/pl/';
require $PL_DIR.'RecordAccessLog.pl';
require $PL_DIR.'MyEscape.pl';
# require $PL_DIR.'EscapeHtml.pl';

my $ACCESS_LOG = &sub::RecordAccessLog($PAGE);

my $DATABASE_FILE = $DIR.'../etc/setting/gallery/imageDatabase.dat';
my $IMG_NUM = 100;		# 1ページに表示する写真数
# my $IMG_NUM = 20;		# 1ページに表示する写真数


####################
# get,post 受け取り
####################
# my $buffer = 0;
# if ($ENV{'REQUEST_METHOD'} eq "POST") {
# 	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
# } else {
# 	$buffer = $ENV{'QUERY_STRING'};
# 	#print 'Location: ./index.html', "\n\n";
# }

# my ($pair, @pairs, %FORM);
# $FORM{'t'} = 'random';		# target
# $FORM{'p'} = '1';			# page
# @pairs = split(/&/, $buffer);
# foreach $pair (@pairs) {
# 	my ($key, $value) = split(/=/, $pair);
# 	$value =~ tr/+/ /;
# 	$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
# 	$FORM{$key} = $value;
# }

# my $target = &sub::EscapeHtml($FORM{'t'});
# my $page   = &sub::EscapeHtml($FORM{'p'});















# データベース読み込み
my @Databases;
if (open(IPF, "<:utf8", $DATABASE_FILE)) {
	my @Datalines = <IPF>;
	for (my $i = 0; $i <= $#Datalines; $i++) {
		$Datalines[$i] =~ s/\r\n$|\r$|\n$//;
		my @Temp = split(/,/, $Datalines[$i]);
		my %TEMP;
		$TEMP{'name'}   = $Temp[0];
		$TEMP{'onoff'}  = $Temp[1];
		$TEMP{'date'}   = $Temp[2];
		$TEMP{'model'}  = $Temp[3];
		$TEMP{'Fval'}   = $Temp[4];
		$TEMP{'exTime'} = $Temp[5];
		$TEMP{'iso'}    = $Temp[6];
		$TEMP{'length'} = $Temp[7];
		# $TEMP{'place'}  = $Temp[8];
		$TEMP{'place'}  = &sub::MyEscape::Unescape($Temp[8]);

		if ($TEMP{'onoff'} eq '1') {
			$Databases[$#Databases + 1] = \%TEMP;
		}
	}
} else {
	exit(1);
}
if (close(IPF)) {
	# なにもしない
} else {
	exit(1);
}

my $maxPageNum = int($#Databases / $IMG_NUM) + 1;




print "content-type: text/html;charset=utf-8\n\n";

print <<'EOM';

<!DOCTYPE html>
<html lang="ja">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<title>溶けかけてるうさぎ - GALLERY</title>
	<meta name="format-detection" content="telephone=no">
	<meta NAME="ROBOTS" CONTENT="NOINDEX,NOFOLLOW,NOARCHIVE">
	<!--
	レスポンシブデザインなどに必要なviewport設定
	http://qiita.com/ryounagaoka/items/045b2808a5ed43f96607
	http://ichimaruni-design.com/2015/01/viewport/
	-->
	<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0">
	<!--<link href="./css/style_article.css" type="text/css" rel="stylesheet">-->
	<!--<link href="./css/navi.css" type="text/css" rel="stylesheet">-->
EOM
	print '<link href="'.$DIR.'css/style_default.css" type="text/css" rel="stylesheet">', "\n";
	print '<link href="./css/style_gellery.css" type="text/css" rel="stylesheet">', "\n";
	print '<link href="'.$DIR.'css/style_toggle.css" type="text/css" rel="stylesheet">', "\n";
	print '<link rel="shortcut icon" href="'.$DIR.'img/favicon.ico" type="image/vnd.microsoft.icon">', "\n";
	# print '<script type="text/javascript" src="'.$DIR.'js/jquery-1.11.2.min.js"></script>', "\n";
	print '<script type="text/javascript" src="'.$DIR.'js/jquery-3.2.0.min.js"></script>', "\n";
	print '<script type="text/javascript" charset="UTF-8" src="./js/script.js"></script>', "\n";
	print '<script type="text/javascript" charset="UTF-8" src="'.$DIR.'js/script_toggle.js"></script>', "\n";


	# print '<link rel="stylesheet" type="text/css" href="'.$DIR.'etc/lightbox/resource/lightbox.css" media="screen,tv" />', "\n";
	# print '<script type="text/javascript" charset="UTF-8" src="'.$DIR.'etc/lightbox/resource/lightbox_plus.js" id="lightboxJS"></script>', "\n";

	print '<link rel="stylesheet" type="text/css" href="'.$DIR.'etc/Magnific-Popup-master/dist/magnific-popup.css" media="screen,tv" />', "\n";
	print '<script type="text/javascript" charset="UTF-8" src="'.$DIR.'etc/Magnific-Popup-master/dist/jquery.magnific-popup.js"></script>', "\n";


print <<'EOM';


	<!-- ページ内移動をスムーズに -->
	<script type="text/javascript">
	$(function(){
		$("a[href^='#']").click(function(){
			var speed = 300;
			var href= $(this).attr("href");
			var target = $(href == "#" || href == "" ? 'html' : href);
			var position = target.offset().top;
			$("html, body").animate({scrollTop:position}, speed, "swing");
			return false;
		});
	});
	</script>


<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-96430472-1', 'auto');
  ga('send', 'pageview');

</script>

</head>

<body>

<div class="SP" id="menubar">
	<header>
		<div id="menuBoxDummy"></div>
	</header>
	<nav class="SP" id="menuBox">
		<div id="toggle">
			<a href="/"><img class="logo" src="/img/Logo_en.png"></a>
		</div>
		<ul id="menu">
			<li><a href="/">Home</a></li>
			<li><a href="/gallery/">Gallery</a></li>
		</ul>
	</nav>
</div>

<nav class="PC" id="menubar">
	<div class="clearfix">
		<div class="left">
			<a href="/"><img class="logo" src="/img/Logo_en.png"></a>
		</div>
		<div class="left">
			<ul>
			<li><a href="/">HOME</a></li>
			<li><a href="/gallery/">GALLERY</a></li>
			</ul>
		</div>
	</div>
</nav>


<div id="controlPanel" class="control-panel clearfix">
	<div id="mainPanel" class="left">
		<div class="left">
			<select name="type">
				<option value="rand" selected>ランダム</option>
				<option value="down">日付 降順</option>
				<option value="up"  >日付 昇順</option>
			</select>
		</div>
		<div class="clearfix left">
			<div class="left"><button type="button" class="page-down">&lt;&lt;</button></div>
			<div class="left" name="page">
EOM
				# <input type="number" name="page" min="1" max="10" step="1" value="1">&nbsp;/&nbsp;20
				# <input type="hidden" name="IMG_NUM" value="60">
print '			<input type="number" name="page" min="1" max="'.$maxPageNum.'" step="1" value="1">&nbsp;/&nbsp;<span id="maxPageNum">'.$maxPageNum.'</span>', "\n";
print '			<input type="hidden" name="IMG_NUM" value="'.$IMG_NUM.'">', "\n";
print <<'EOM';
			</div>
			<div class="left"><button type="button" class="page-up">&gt;&gt;</button></div>
		</div>
		<div class="left go-button">
			<div class="left"><button type="button" id="goButton">GO!</button></div>
		</div>
	</div>
	<div id="subPanel" class="left">
		<div class="left">
EOM
			# seed : <span id="seed">123</span>
print '		seed : <span id="seed">'.int(rand(100000)).'</span>', "\n";
print <<'EOM';
		</div>
		<div class="left">
			<button type="button" id="changeButton">CHANGE</button>
		</div>
	</div>
</div>

<div id="imageArea" class="clearfix">
EOM

# lightbox Plus の場合
# foreach (@Databases) {
# 	my $dateRaw = ${$_}{'date'};
# 	# 01234567890123
# 	# 20170315201048
# 	my $date = substr($dateRaw,0,4).'.'.substr($dateRaw,4,2).'.'.substr($dateRaw,6,2).' ';
# 	$date   .= substr($dateRaw,8,2).':'.substr($dateRaw,10,2);
# 	my @Temp = split(/\s/, ${$_}{'length'});
# 	my $len = $Temp[0];
# 	print '<div class="photo_container left">', "\n";
# 	print '    <img class="photo" src="./img/S/'.${$_}{'name'}.'">', "\n";
# 	print '    <a href="./img/M/'.${$_}{'name'}.'" rel="lightbox[c]" title="'.$date.' F/'.${$_}{'Fval'}.' '.$len.'mm '.${$_}{'exTime'}.'s '.${$_}{'iso'}.'"><img class="X" src="./img/Xw.png"></a>', "\n";
# 	print '    <div class="imgDummy"></div>', "\n";
# 	print '    <div class="description">', "\n";
# 	print '        <p>'.$date.'</p>', "\n";
# 	print '        <p>'.${$_}{'model'}.'</p>', "\n";
# 	print '        <p>F/'.${$_}{'Fval'}.'</p>', "\n";
# 	print '        <p>'.${$_}{'length'}.'</p>', "\n";
# 	print '        <p>'.${$_}{'exTime'}.' s</p>', "\n";
# 	print '        <p>ISO '.${$_}{'iso'}.'</p>', "\n";
# 	print '        <p>'.${$_}{'place'}.'</p>', "\n";
# 	print '    </div>', "\n";
# 	print '</div>', "\n";
# }


# Magnific Popup の場合
# foreach (@Databases) {
# 	my $dateRaw = ${$_}{'date'};
# 	# 01234567890123
# 	# 20170315201048
# 	my $date = substr($dateRaw,0,4).'.'.substr($dateRaw,4,2).'.'.substr($dateRaw,6,2).' ';
# 	$date   .= substr($dateRaw,8,2).':'.substr($dateRaw,10,2);
# 	my @Temp = split(/\s/, ${$_}{'length'});
# 	my $len = $Temp[0];
# 	print '<div class="photo_container left">', "\n";
# 	print '    <img class="photo" src="./img/S/'.${$_}{'name'}.'">', "\n";
# 	print '    <a href="./img/M/'.${$_}{'name'}.'" rel="lightbox[c]" title="'.$date.' F/'.${$_}{'Fval'}.' '.$len.'mm '.${$_}{'exTime'}.'s '.${$_}{'iso'}.'"><img class="X" src="./img/Xw.png"></a>', "\n";
# 	print '    <div class="imgDummy"></div>', "\n";
# 	print '    <div class="description">', "\n";
# 	print '        <p>'.$date.'</p>', "\n";
# 	print '        <p>'.${$_}{'model'}.'</p>', "\n";
# 	print '        <p>F/'.${$_}{'Fval'}.'</p>', "\n";
# 	print '        <p>'.${$_}{'length'}.'</p>', "\n";
# 	print '        <p>'.${$_}{'exTime'}.' s</p>', "\n";
# 	print '        <p>ISO '.${$_}{'iso'}.'</p>', "\n";
# 	print '        <p>'.${$_}{'place'}.'</p>', "\n";
# 	print '    </div>', "\n";
# 	print '</div>', "\n";
# }

print <<'EOM';

</div>

<div id="controlPanelBottom" class="control-panel clearfix">
	<div id="bottomPanel" class="left">
		<div class="clearfix left">
			<div class="left"><button type="button" class="page-down">&lt;&lt;</button></div>
			<div class="left" name="page">
EOM
				# <input type="number" name="page" min="1" max="10" step="1" value="1">&nbsp;/&nbsp;20
				# <input type="hidden" name="IMG_NUM" value="60">
print '			<input type="number" name="page" min="1" max="'.$maxPageNum.'" step="1" value="1">&nbsp;/&nbsp;<span id="maxPageNum">'.$maxPageNum.'</span>', "\n";
print '			<input type="hidden" name="IMG_NUM" value="'.$IMG_NUM.'">', "\n";
print <<'EOM';
			</div>
			<div class="left"><button type="button" class="page-up">&gt;&gt;</button></div>
		</div>
	</div>
</div>


<footer>
<p>Copyright&copy;&nbsp;&nbsp; <a href="/">溶けかけてるうさぎ MeltingRabbit</a>&nbsp;&nbsp; All Rights Reserved.</p>
</footer>


</body>
</html>


EOM



exit;

