#!C:\Perl\bin\perl.exe

# FTOWA.com News Grabber Script
# -------------------------------
use LWP::Simple;


#########################################################
# AUTOSPEED GRABBER
# -----------------
# Autospeed plays very nicely to spiders :) each article
# link has its own class, making it easy to find titles
# and links to the articles.
#########################################################

$counter = 1;
$lastLinkIndex = 0;
$AutoSpeedURL = "http://www.autospeed.com/index.html";

# get autospeed URL and parse for links.
# generate as.html for inclusion into ftowa website
$httpText = get($AutoSpeedURL);

# Autospeed use an "articleLink" class for all article headers. this class
# exists in the actual HREF so we can simply grab all of it including text
$newsGroup = &startTableHTML("AutoSpeed Latest");
for ($counter = 1; $counter <= 5; $counter++)
    {
    # find the article link
    $lastLinkIndex  = index $httpText, "articleLink", $lastLinkIndex;
    $startLinkIndex = rindex $httpText, "<", $lastLinkIndex;
    $endLinkIndex   = index($httpText, "</A>", $lastLinkIndex) + 4;
    $lastLinkIndex = $endLinkIndex;
    $articleLink = substr($httpText, $startLinkIndex, $endLinkIndex - $startLinkIndex);

    # we need to prepent http://www.autospeed.com/ to the front of the URL
    $preURL       = substr($articleLink, 0, index($articleLink, "HREF=") + 6);
    $postURL      = substr($articleLink, index($articleLink, "HREF=") + 6);
    $articleLink  = $preURL . "http://www.autospeed.com" . $postURL;
    $preURL       = substr($articleLink, 0, index($articleLink, "CLASS="));
    $postURL      = substr($articleLink, index($articleLink, "CLASS="));
    $articleLink  = $preURL . "TARGET='Autospeed'" . $postURL;

    # create this TD section
    $newsGroup = $newsGroup . "      <font size='2'>$articleLink<br></font>\n";

    }

# add a simulated autospeed searcher
#$newsGroup = $newsGroup .   "<FORM METHOD=GET ACTION='http://www.autospeed.com/cms/search/index.html'>" .
#                            "  <input type='text' name='keywords'>" .
#                            "  <input type='submit' name='Search'><BR>" .
#                            "</FORM>";

$newsGroup = $newsGroup . &endTableHTML();

open ASFILE, ">../html/ASNews.html";
print ASFILE $newsGroup;
close ASFILE;

#########################################################
# END AUTOSPEED GRABBER
#########################################################


#########################################################
# Syndic8 Automotive News Feed
# ----------------------------
# Just what we're after, an XML RSS feed for auto news!
# what more could we ask for? well not much really :)
#########################################################

$counter = 1;
$lastLinkIndex = 0;
$SyndicURL = "http://www.autosinfo.com/news/feed/news.cfm";

# get autospeed URL and parse for links.
# generate as.html for inclusion into ftowa website
$httpText = get($SyndicURL);

# Autospeed use an "articleLink" class for all article headers. this class
# exists in the actual HREF so we can simply grab all of it including text
$newsGroup = &startTableHTML("Latest Autosinfo.com News");
for ($counter = 1; $counter <= 5; $counter++)
    {
    $lastLinkIndex  = index $httpText, "item", $lastLinkIndex;

    # find article title
    $lastLinkIndex  = index $httpText, "title", $lastLinkIndex;
    $startLinkIndex = rindex($httpText, "<", $lastLinkIndex) + 7;
    $endLinkIndex   = index $httpText, "</title>", $lastLinkIndex;
    $lastLinkIndex = $endLinkIndex;
    $articleTitle = substr($httpText, $startLinkIndex, $endLinkIndex - $startLinkIndex);

    # find the article link
    $lastLinkIndex  = index $httpText, "link", $lastLinkIndex;
    $startLinkIndex = rindex($httpText, "<", $lastLinkIndex) + 6;
    $endLinkIndex   = index $httpText, "</link>", $lastLinkIndex;
    $lastLinkIndex = $endLinkIndex;
    $articleLink = substr($httpText, $startLinkIndex, $endLinkIndex - $startLinkIndex);

    # create this TD section
    $newsGroup = $newsGroup . "      <font size='2'><a href='$articleLink' target='autosinfo'>$articleTitle</a><br></font>\n";
    }

$newsGroup = $newsGroup . &endTableHTML();

open ASFILE, ">../html/AutoNews.html";
print ASFILE $newsGroup;
close ASFILE;

#########################################################
# END SYNDIC8 GRABBER
#########################################################

sub startTableHTML #()
    {
    (my $sTHTitle) = @_;
    return  "<head>" .
            "<link rel='stylesheet' href='css/mainStyle.css' type='text/css'>" .
            "</head>" .
            "<body bgcolor='#003399' text='#FFFFFF' link='#FFFFFF' vlink='#FFFFFF' alink='#FFFFFF' leftmargin='0' topmargin='0' marginwidth='0' marginheight='0'>" .
            "<table width='100%'>\n" .
            "  <tr>\n" .
            "    <td bgcolor='#200040'>\n" .
            "      <font size='2'>$sTHTitle</font>\n" .
            "    </td>\n" .
            "  </tr>\n" .
            "  <tr>\n" .
            "    <td>\n" .
            "      <p>\n";

    }

sub endTableHTML #()
    {
    return  "      </p>\n" .
            "    </td>\n" .
            "  </tr>\n" .
            "</table>\n" .
            "</body>\n";
    }
