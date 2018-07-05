
# これはヘッダー
# print "content-type: text/html;charset=utf-8\n\n";
# を送信する前に実行すること．
# そうすれば，エラーのexitでInternal Server Errorを出せる．

use utf8;
package sub;
sub OutputFile {
	my $outputFile = $_[0];
	my $outputStr = $_[1];

	my $PL_DIR = "/var/www/etc/pl/";
	my $OUT_DIR = '/var/www/etc/output/';
	require $PL_DIR.'GetStringTime.pl';
	my $stime = &sub::GetStringTime();

	$outputFile = $OUT_DIR.$outputFile.'_'.$stime.'.txt';
	&sub::OutputFile::OutputFile($outputFile, $outputStr);

	my $tweetStr = "";
	$tweetStr .= "\@_szmt \n";
	$tweetStr .= $stime."\n";
	$tweetStr .= "cmnt!!\n";
	# $tweetStr .= $_[0]."!!\n";

	&sub::OutputFile::Tweet($tweetStr);
	# my $command = 'python "/home/share/script/twitter/tweet.py" "'.'hogehoge'.'"';
	# my @CommandResult = `$command`;

	# &sub::OutputFile::OutputFile('/home/share/script/twitter/logpy.log', &sub::OutputFile::Tweet("hogehoge"));

}

package sub::OutputFile;

sub OutputFile {
	my $filename = $_[0];
	my $str      = $_[1];
	open(FH,">> ".$filename) or die("Error:$!");
	print FH $str;
	close(FH);
	return 1;
}

# package sub::OutputFile;

sub Tweet {
	my $command = 'python "/home/share/script/twitter/tweet.py" "'.$_[0].'"';
	my @CommandResult = `$command`;
	return $CommandResult[0];
}


1;

