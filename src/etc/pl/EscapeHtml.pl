
use utf8;
package sub;
sub EscapeHtml {
	my $str = shift || return(undef);
	$str =~ s/&/&amp;/g;
	$str =~ s/</&lt;/g;
	$str =~ s/>/&gt;/g;
	$str =~ s/\"/&quot;/g;
	$str =~ s/\'/&#39;/g;
	return ($str);
}


1;

