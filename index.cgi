#!/usr/bin/perl -wT
use strict;
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use DBI;
use JSON;

my $dbh = DBI->connect(          
    "dbi:mysql:dbname=requestbin", 
    "root",
    "N0cand0a",
    { RaiseError => 1}
) or die $DBI::errstr;


my $query  				= new CGI ;
my @names  				= $query->param ;
my $form_result;
my $env_result;
my $payload;
my $list;
my $envstuff = encode_json \%ENV;
my $test = 0;
$test = $query->param("view");

 my %temp = ();
sub compile_form_info {
	$form_result = "\t\t<tr><td colspan=2><b><font color='red'>Form results:</td></tr>\n";
	$form_result .= "\t\t<tr><td><b><font color='blue'>Name</td><td><b><font color='blue'>Value</td></tr>\n";
	for my $n (0 .. $#names) {	
		my @values = $query->param ($names[$n]);
		for my $v (0 .. $#values) {	
			$form_result .= "   <tr><td>$names[$n]</td><td>" . $values[$v] . "</td></tr>\n";
			$temp{$names[$n]} = $values[$v];
		}
	}
	$payload = to_json \%temp;
}

sub compile_env_vars {
	$env_result = "\t\t<tr><td colspan=2><b><font color='red'>Environment Vars:</td></tr>\n";
	$env_result.= "\t\t<tr><td><b><font color='blue'>Key</td><td><b><font color='blue'>Value</td></tr>\n";
	foreach my $key (keys(%ENV)) {
		$env_result .= "   <tr><td>$key</td><td>" . $ENV{$key} . "</td></tr>\n";
	}
}

sub item_HTML {
print $query->header();
print $query->start_html(
        -title => 'Environment',
        -bgcolor => 'white',
);
	print <<END ;
 <body>
  <p><table border=1 cellspacing="3" cellpadding="3" width="300">
$env_result
  </table>
  <p>
  <table border=1 cellspacing="3" cellpadding="3" width="300">
$form_result
  </table>
END
print $query->end_html;
}

sub list_HTML {
print $query->header();
print $query->start_html(
        -title => 'Environment',
        -bgcolor => 'white',
);
	print <<END ;
 <body>
  <p><table border=1 cellspacing="3" cellpadding="3" width="300">
$list
  </table>
END
print $query->end_html;
}

sub record_data {

$dbh->do("INSERT INTO InComing(Data,Payload) VALUES('".$envstuff."','".$payload."')");
$dbh->disconnect();

}

sub get_list_data {

my $sth = $dbh->prepare( "SELECT * FROM InComing" );  
$sth->execute();
my $row;
while ($row = $sth->fetchrow_arrayref()) {
    $list .= "<tr><td>@$row[0]</td><td>@$row[1]</td><td>@$row[2]</td><td>@$row[3]</td><td>@$row[4]</td></tr>\n";
}
}

compile_form_info();
compile_env_vars();
if ($test) {
get_list_data();
list_HTML();
} else {
record_data();
item_HTML();
}

1;
