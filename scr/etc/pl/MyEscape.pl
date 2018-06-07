
use utf8;
package sub;

package sub::MyEscape;

sub Escape {
	my $str = shift || return(undef);
	$str =~ s/#/##/g;
	$str =~ s/,/#c/g;
	return($str);
}

sub Unescape {
	my $str = shift || return(undef);
	$str =~ s/##/#/g;
	$str =~ s/#c/,/g;
	return($str);
}


# sub EscapeHtml {
	# my $str = shift || return(undef);
# 	$str =~ s/&/&amp;/g;
# 	$str =~ s/</&lt;/g;
# 	$str =~ s/>/&gt;/g;
# 	$str =~ s/\"/&quot;/g;
# 	$str =~ s/\'/&#39;/g;
# 	return($str);
# }


1;

