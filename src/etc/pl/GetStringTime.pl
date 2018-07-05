
use utf8;
package sub;
use Time::Local;
use Time::HiRes qw/ gettimeofday /;
sub GetStringTime {

	my ($epocsec, $microsec) = gettimeofday();
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($epocsec);
	$year += 1900;
	$mon += 1;
	#printf("%020d:\n",12345678);
	return sprintf("%04d.%02d.%02d-%02d.%02d.%02d.%06d",$year,$mon,$mday,$hour,$min,$sec,$microsec);

}


1;

