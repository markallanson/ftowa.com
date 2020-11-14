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

# standard member information
$fields{"name"}     = $list{$fields{"member"} . "name"} . " (" . $fields{"member"} . ")";

# only show if not blank
if ($list{$fields{"member"} . "website"} ne "")
    {
    $fields{"website"}  = "<A HREF='" . $list{$fields{"member"} . "website"} . "' TARGET='WEBSITE'>Visit Website</A>";
    }

# dont show if they have requested not to show.
if ($list{$fields{"member"} . "dontshow"} ne "yes")
    {
    $fields{"email"}    = "<A HREF='mailto:" . $list{$fields{"member"} . "email"} . "'>Contact</A>";
    }

$fields{"car"}      = $list{$fields{"member"} . "car"};

# search and replace ~ charactrers with <BR>'s for HTML display
$list{$fields{"member"} . "mods"} =~ s/~/<BR>/g;
$list{$fields{"member"} . "comment"} =~ s/~/<BR>/g;

$fields{"mods"}     = $list{$fields{"member"} . "mods"};
$fields{"comments"} = $list{$fields{"member"} . "comment"};

# Picture code to generate the picture page.. maybe make this product more detailed
# HTML so we can have more than 6 pics if wanted.. but if so, where do we stop.
# im to lazy to make a variable picture adder type thingo
if ($list{$fields{"member"} . "picture1"} ne "")
    {
    $fields{"pic1"} = "<A HREF='" . $list{$fields{"member"} . "picture1"} . "' TARGET='PIX'><IMG SRC='" . $list{$fields{"member"} . "picture1"} . "' WIDTH='120' HEIGHT='80' BORDER=1></a>\n";
    }
else
    {
    $fields{"pic1"} = "<A HREF='/cgi-bin/profileedit.cgi?member=" . $fields{"member"} . "&remote=TRUE'>Add Picture<A>\n";
    }

if ($list{$fields{"member"} . "picture2"} ne "")
    {
    $fields{"pic2"} = "<A HREF='" . $list{$fields{"member"} . "picture2"} . "' TARGET='PIX'><IMG SRC='" . $list{$fields{"member"} . "picture2"} . "' WIDTH='120' HEIGHT='80' BORDER=1></A>\n";
    }
else
    {
    $fields{"pic2"} = "<A HREF='/cgi-bin/profileedit.cgi?member=" . $fields{"member"} . "&remote=TRUE'>Add Picture<A>\n";
    }

if ($list{$fields{"member"} . "picture3"} ne "")
    {
    $fields{"pic3"} = "<A HREF='" . $list{$fields{"member"} . "picture3"} . "' TARGET='PIX'><IMG SRC='" . $list{$fields{"member"} . "picture3"} . "' WIDTH='120' HEIGHT='80' BORDER=1></a>\n";
    }
else
    {
    $fields{"pic3"} = "<A HREF='/cgi-bin/profileedit.cgi?member=" . $fields{"member"} . "&remote=TRUE'>Add Picture<A>\n";
    }

if ($list{$fields{"member"} . "picture4"} ne "")
    {
    $fields{"pic4"} = "<A HREF='" . $list{$fields{"member"} . "picture4"} . "' TARGET='PIX'><IMG SRC='" . $list{$fields{"member"} . "picture4"} . "' WIDTH='120' HEIGHT='80' BORDER=1></a>\n";
    }
else
    {
    $fields{"pic4"} = "<A HREF='/cgi-bin/profileedit.cgi?member=" . $fields{"member"} . "&remote=TRUE'>Add Picture<A>\n";
    }

if ($list{$fields{"member"} . "picture5"} ne "")
    {
    $fields{"pic5"} = "<A HREF='" . $list{$fields{"member"} . "picture5"} . "' TARGET='PIX'><IMG SRC='" . $list{$fields{"member"} . "picture5"} . "' WIDTH='120' HEIGHT='80' BORDER=1></a>\n";
    }
else
    {
    $fields{"pic5"} = "<A HREF='/cgi-bin/profileedit.cgi?member=" . $fields{"member"} . "&remote=TRUE'>Add Picture<A>\n";
    }

if ($list{$fields{"member"} . "picture6"} ne "")
    {
    $fields{"pic6"} = "<A HREF='" . $list{$fields{"member"} . "picture6"} . "' TARGET='PIX'><IMG SRC='" . $list{$fields{"member"} . "picture6"} . "' WIDTH='120' HEIGHT='80' BORDER=1></a>\n";
    }
else
    {
    $fields{"pic6"} = "<A HREF='/cgi-bin/profileedit.cgi?member=" . $fields{"member"} . "&remote=TRUE'>Add Picture<A>\n";
    }




$fields{"editmessage"} = "Are you " . $fields{"member"} . "? You can <A HREF='/cgi-bin/profileedit.cgi?member=" . $fields{"member"} . "&remote=TRUE'>edit your details<A> if they are out of date.";

&ptHTML::displayHTML("../html/memberprofiletemplate.html", %fields);


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