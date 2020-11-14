#!C:\Perl\bin\perl.exe
##
## FMAIL - Simple form mailer
##
## Mails all fields on a form to an email account. Will /not/ check for missing
## or blank fields, but will check for no fields.
##
## This script is free to use and modify under GPL.
##
## (C) 2002, Mark Allanson
##

use CGI qw(:standard);

$|     = 1;
$login = $ENV{"REMOTE_USER"};

###############################################################################
## User Defined Variables
###############################################################################
# Who should we send the mail to? multiple addresses can be used
# by seperating with the ; character
$mailTo         = "marke\@iinet.net.au";
# The mail should look like its comming from the webpage of the client.
# you might wanna figure this out by parsing parameters on a the form?
$mailFrom       = "<SK DESIGNS>";
# this should be set to whatever you want the subject line of the email to
# appear like.
$mailSubject    = "FMAIL Form Mail Program";
# The following line will set which mail program to use to send email from the
# website. On most unix systems setting $mailProg to `which sendmail` should
# find the sendmail program automatically, however on ozehosts it does not
# work, and you must set $mailProg to "/usr/sbin/sendmail" instead. If you move
# to a different server and, don't know the location of the sendmail program,
# using the first instance should work.
#$mailProg       = `which sendmail`;
$mailProg       = "/usr/sbin/sendmail";     # ozehosts uses /usr/sbin

# where should we go to after mail finshed? (this can be any URL)
$reDirectPage   = "/success.html";

# where should we send them if they didnt fill out any of the form?
# (this can be any URL)
$noParamPage    = "/noparams.html";

# this will be displayed before a listing of the fields on the form
$mailHeader     = "Someone has filled out a form on your website. Attached " .
                  "are the details contained within the form.\n\n";

# mail footer, will be displayed at the end of the email, after the field list
$mailFooter     = "\nThank you,\n\nFMAIL BOT";

###############################################################################
## Static Variables, No need to change these.
###############################################################################
$mailTime       = localtime(time);  # sets the time the form was submitted
$paramCount     = 0;                # how many parameters passed through

###############################################################################
## Code starts here.
###############################################################################

$emailBody = $mailHeader;

# loop through all fields in the form, add them to the email
# set the parameters
foreach $field (&param())
    {
    foreach $value (&param($field))
        {
        $emailBody = $emailBody . $field . ": " . $value . "\n";
        $paramCount += 1
        }
    }

if ($paramCount = 0)
    {
    goToPage($noParamPage);
    }

$emailBody = $emailBody . $mailFooter;

# send the composed email
sendMail($mailTo, $mailFrom, $mailSubject, $emailBody);

goToPage($reDirectPage);


###############################################################################
## Send the form fields in an email
###############################################################################
sub sendMail #()
    {
    my ($to, $from, $subject, @text) = @_;

    # If using `which sendmail` to determine location of sendmail, this will
    # get rid of the trailing EOL
    chomp $mailProg;

    # tell web browser to ignore any output. depending on where you call
    # this function the web browser may or may not be expecing HTML comments..
    # it shouldn't matter either way.
#    print "<!--";

    if (open MAIL, "|$mailProg -i -t")
        {
        print MAIL "To: $to\n",
                   "From: $from\n",
                   "Subject: $subject\n",
                   "@text\n\n";
        close MAIL;
        }

#    print "-->\n";

    }


###############################################################################
## will display a "success" type web page after the form has been filled out
## successfully.
###############################################################################
sub goToPage #($fileName)
    {
    my ($fileName) = @_;
    my $line;

    print("Content-type: text/html\n\n");
    print("<HTML>");
    print("<!-- FMAIL PAGE REDIRECT -->");
    print("<META HTTP-EQUIV='REFRESH' CONTENT='0; URL=$fileName'>");
    print("</HTML>");
    }


