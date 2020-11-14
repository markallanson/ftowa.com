#!C:\Perl\bin\perl.exe

use CGI qw(:standard);
use ptHTML;
use ptDIO;


&ptHTML::startHTML();

$|          = 1;
$nickname   = $ENV{"REMOTE_USER"};
$ptTime     = localtime(time);
$params     = &loadParameters();

# load member detials file.
%list = &ptDIO::loadFile("members");

&listMembers( &ptDIO::loadFileIntoList( "members" ) );

sub sortmember
    {
#    my ($a, $b) = @_;
#    print "<p>" . $a . " - " . $b . "</p>";

#    if ($a{"name"} eq $b{"name"})
        return 0;
#    elsif ($a{"name"} gt $b{"name"})
#        return 1;
#    else
#        return -1;
    }

sub listMembers #(users)
    {
    my @users       = @_;
    my $memberCount  = 0;

    $membersList = "<TABLE align='center' width='90%'><TR><TD width = 25%>&nbsp;</TD><TD width='40%'>&nbsp</TD><TD width='25%'>&nbsp</TD></TR>\n";

    foreach $user (sort(sortmember @users))
        {
        my ($data, $value) = split("=", $user);

        chomp($value); # get rid of trailing CRLF

        # if the value to the right of the = sign is 1, then the data must be the member name
        if ($value eq "1")
            {

            $membersList = $membersList . "<TR><TD><A HREF='/cgi-bin/showprofile.cgi?member=$data'><FONT SIZE='2'><B>" . $list{$data . "name"} . "</B></FONT></A></TD><TD><FONT SIZE='2'>" . $list{$data . "car"} . "</FONT></TD><TD>";

            # only show email if they have given permission
            if ($list{$data . "dontshow"} ne "yes")
                {
                $membersList = $membersList . "<A HREF='mailto:" . $list{$data . "email"}. "'><FONT SIZE='2'>Contact</FONT></A> | ";
                }
            # if website is blank, point to profile page
            if ($list{$data . "website"} ne "")
                {
                $membersList = $membersList . "<A HREF='" . $list{$data . "website"}. "' target='$data'><FONT SIZE='2'>Visit</FONT></A>";
                }
            else
                {
                $membersList = $membersList . "<A HREF='/cgi-bin/showprofile.cgi?member=$data'><FONT SIZE='2'>Visit</FONT></A>\n";
                }

            $membersList = $membersList . " | <A HREF='/cgi-bin/showprofile.cgi?member=$data'><FONT SIZE='2'>Profile</FONT></A></TD></TR>\n";
            $memberCount++;

            }
        }

    $membersList = $membersList . "<TR><TD></TD><TD></TD><TD></TD></TR>\n";
    $membersList = $membersList . "<TR><TD></TD><TD><FONT SIZE='2'>Total Members:</FONT></TD><TD><FONT SIZE='2'>$memberCount</FONT></TD></TR>\n";
    $membersList = $membersList . "</TABLE>\n";

    # add it to the fields list. display the member list
    $fields{"memberlist"} = $membersList;

    &ptHTML::displayHTML("../html/memberlisttemplate.html", %fields);

    }


sub loadParameters #()
    {
    my $result = 0;

    # set the parameters
    foreach $field (sort(&param()))
        {
        foreach $value (&param($field))
            {
            $fields{$field} = $value;
            $result += 1;
            }
        }

    # set some must-haves
    $fields{"REMOTE_USER"} = $ENV{"REMOTE_USER"};

    return $result;
    }
