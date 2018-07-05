#!/usr/bin/perl

use strict;
use warnings;
use utf8;
binmode STDOUT, ':utf8';

my $DIR = "../../";
my $PAGE = "gallery/cgi/getImageArea.cgi";

my $PL_DIR = $DIR.'../etc/pl/';
# require $PL_DIR.'GetStringTime.pl';
require $PL_DIR.'RecordAccessLog.pl';
require $PL_DIR.'EscapeHtml.pl';
require $PL_DIR.'MyEscape.pl';
# require $PL_DIR.'OutputFlie.pl';

my $ACCESS_LOG = &sub::RecordAccessLog($PAGE);


# &Err();


####################
# get,post 受け取り
####################
my $buffer = 0;
if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
} else {
	$buffer = $ENV{'QUERY_STRING'};
	exit;
	#print 'Location: ./index.html', "\n\n";
}

my ($pair, @pairs, %FORM);
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
	my ($key, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
	# $FORM{$key} = $value;
	$FORM{$key} = &sub::EscapeHtml($value);
}

# keyがあるか確認必須！
if (!(exists($FORM{'IMG_NUM'}))) {
	&Err();
}
if (!(exists($FORM{'type'}))) {
	&Err();
}
if (!(exists($FORM{'page'}))) {
	&Err();
}
if (!(exists($FORM{'seed'}))) {
	&Err();
}

my $type      = &sub::EscapeHtml($FORM{'type'});
my $page      = &sub::EscapeHtml($FORM{'page'});
my $seed      = &sub::EscapeHtml($FORM{'seed'});
my $IMG_NUM   = &sub::EscapeHtml($FORM{'IMG_NUM'});
if ($IMG_NUM <= 0) {
	$IMG_NUM = 1;
}


$page = int($page);

my $result = "";


my $DATABASE_FILE = $DIR.'../etc/setting/gallery/imageDatabase.dat';

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
if ($page < 1) {
	$page = 1;
}
if ($page > $maxPageNum) {
	$page = $maxPageNum;
}


# 並び替え
if ($type eq 'up') {
	@Databases = sort {${$a}{'date'} <=> ${$b}{'date'}} @Databases;
} elsif ($type eq 'down') {
	@Databases = sort {${$b}{'date'} <=> ${$a}{'date'}} @Databases;
} else {
	# ランダム
	srand($seed);
	foreach (@Databases) {
		${$_}{'rand'} = rand();
	}
	@Databases = sort {${$a}{'rand'} <=> ${$b}{'rand'}} @Databases;
}

$result .= <<'EOM';
EOM

# テストコード
# $result .= '<p>'.$IMG_NUM.'</p>';
# $result .= '<p>'.$page.'</p>';
# $result .= '<p>'.$type.'</p>';
# $result .= '<p>'.$seed.'</p>';


# $result .= '<div id="testhoge">';
# foreach (@Databases) {
# for (my $i = 0; $i <= $#Databases; $i++) {
for (my $i = $IMG_NUM * ($page-1); $i < $IMG_NUM * ($page); $i++) {
	if ($i > $#Databases) {
		last;
	}
	my $dateRaw = ${$Databases[$i]}{'date'};
	# 01234567890123
	# 20170315201048
	my $date = substr($dateRaw,0,4).'.'.substr($dateRaw,4,2).'.'.substr($dateRaw,6,2).' ';
	$date   .= substr($dateRaw,8,2).':'.substr($dateRaw,10,2);
	my @Temp = split(/\s/, ${$Databases[$i]}{'length'});
	my $len = " ";		# $Temp[0] が空のときもあるので．ApacheでErrorがでる．
	$len = $Temp[0] if ($Temp[0]);
	$result .= '<div class="photo_container left">'."\n";
	$result .= '    <img class="photo" src="./img/S/'.${$Databases[$i]}{'name'}.'">'."\n";
	$result .= '    <a href="./img/M/'.${$Databases[$i]}{'name'}.'" rel="lightbox[c]" onclick="showLightbox(this); return false;" title="'.$date.' F/'.${$Databases[$i]}{'Fval'}.' '.$len.'mm '.${$Databases[$i]}{'exTime'}.'s '.${$Databases[$i]}{'iso'}.'"><img class="X" src="./img/Xw.png"></a>'."\n";
	$result .= '    <div class="imgDummy"></div>'."\n";
	$result .= '    <div class="description">'."\n";
	$result .= '        <p>'.$date.'</p>'."\n";
	$result .= '        <p>'.${$Databases[$i]}{'model'}.'</p>'."\n";
	$result .= '        <p>F/'.${$Databases[$i]}{'Fval'}.'</p>'."\n";
	$result .= '        <p>'.${$Databases[$i]}{'length'}.'</p>'."\n";
	$result .= '        <p>'.${$Databases[$i]}{'exTime'}.' s</p>'."\n";
	$result .= '        <p>ISO '.${$Databases[$i]}{'iso'}.'</p>'."\n";
	$result .= '        <p>'.${$Databases[$i]}{'place'}.'</p>'."\n";
	$result .= '    </div>'."\n";
	$result .= '</div>'."\n";
}
# $result .= '</div>'."\n";



# これを最後に出すことによって，ここまででエラーが出るとエラーのexitでInternal Server Errorを出せる．
print "content-type: text/html;charset=utf-8\n\n";
# print 100;
# print $IMG_NUM;
print $result;

exit;


sub Err() {
	print "content-type: text/html;charset=utf-8\n\n";
	print -1;
	exit;
}