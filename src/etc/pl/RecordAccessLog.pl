
# これはヘッダー
# print "content-type: text/html;charset=utf-8\n\n";
# を送信する前に実行すること．
# そうすれば，エラーのexitでInternal Server Errorを出せる．

use utf8;
package sub;
sub RecordAccessLog {
	my $accessPage = $_[0];

	# ファイル名にするために
	# / → -
	# ? → #
	# に置換
	my $accessPageFilename = $accessPage;
	$accessPageFilename =~ s/\//\-/g;
	$accessPageFilename =~ s/\?/\#/g;
	$accessPageFilename .= ".log";

	my $LOG_FILE = 'logAll.log';
	my $LOG_BOT_FILE = 'logBot.log';
	my $ERROR_FILE = 'error.log';
	my $LOG_DIR = '/var/www/etc/log/';
	my $LOCK_DIR = "LOCK/";
	my $PL_DIR = "/var/www/etc/pl/";

	my $MAX_TRY_NUM = 10;
	my $TRY_INTERVAL = 1;

	# LANからのアクセスは記録しない．
	if (substr($ENV{'REMOTE_ADDR'}, 0, 11) eq "192.168.10.") {
		return 0;
	}



	require $PL_DIR.'GetStringTime.pl';

	my $stime = &sub::GetStringTime();
	my $log = "";
	$log .= $stime;
	$log .= ','.$ENV{'REMOTE_ADDR'};
	$log .= ','.$ENV{'REMOTE_HOST'};
	$log .= ','.$accessPage;
	$log .= ','.$ENV{'REQUEST_URI'};
	$log .= ','.$ENV{'HTTP_REFERER'};
	$log .= ','.$ENV{'HTTP_FORWARDED'};
	$log .= ','.$ENV{'HTTP_X_FORWARDED_FOR'};
	$log .= ','.$ENV{'HTTP_USER_AGENT'};
	$log .= ','.$ENV{'HTTP_COOKIE'}."\n";


	# ファイルロック
	my $tryCount = 0;
	while (1) {
		$tryCount++;
		if (!mkdir($LOG_DIR.$LOCK_DIR, 0755)) {
			# ロックされていた
			sleep($TRY_INTERVAL);
		} else {
			# ロックされてなかった
			last;
		}
		if ($tryCount >= $MAX_TRY_NUM) {
			&sub::RecordAccessLog::OutputFile($LOG_DIR.$ERROR_FILE, &sub::GetStringTime()."\tFLINE LOCK TIMEOUT at RecordAccessLog.pl\n");
			# Internal Server Error
			exit;
		}
	}


	if (
			   $ENV{'HTTP_USER_AGENT'} =~ /googlebot/i
			|| $ENV{'HTTP_USER_AGENT'} =~ /Google\sSearch\sConsole/i
			|| $ENV{'HTTP_USER_AGENT'} =~ /applebot/i
			|| $ENV{'HTTP_USER_AGENT'} =~ /DotBot/i
			|| $ENV{'HTTP_USER_AGENT'} =~ /bingbot/i
			|| ( $ENV{'HTTP_USER_AGENT'} =~ /Slurp/i && $ENV{'HTTP_USER_AGENT'} =~ /Yahoo/i )
		)
	{
		# 対Bot
		&sub::RecordAccessLog::OutputFile($LOG_DIR.$LOG_BOT_FILE, $log);
	} else {
		# 全ログ
		&sub::RecordAccessLog::OutputFile($LOG_DIR.$LOG_FILE, $log);
		# ページごとのログ
		&sub::RecordAccessLog::OutputFile($LOG_DIR.$accessPageFilename, $log);
	}

	# ファイルロック解除
	rmdir($LOG_DIR.$LOCK_DIR);

	return $log;
}

package sub::RecordAccessLog;

sub OutputFile {
	my $filename = $_[0];
	my $str      = $_[1];
	open(FH,">> ".$filename) or die("Error:$!");
	print FH $str;
	close(FH);
	return 1;
}


1;

