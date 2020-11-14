#!C:\Perl\bin\perl.exe

use CGI qw(:standard);
use ptHTML;
use ptDIO;

&ptHTML::startHTML();

$|     = 1;
$nickname = $ENV{"REMOTE_USER"};

$ptTime       = localtime(time);

$params    = &loadParameters();

if ((!$params) or ($fields{"tc"} ne "yes") or ($fields{"name"} eq "") or ($fields{"email"} eq "") or ($fields{"nickname"} eq ""))
    {
  	$fields{"nicknamemessage"} = "Will also be used as login name.";
    ptHTML::displayHTML("../html/join.html", %fields);
    }
else
    {

    # add member to members flat file.
    %list = &ptDIO::loadFile("members");

    # check to see if member is already taken
    if ($list{"nickname"} == 1 )
        {
    	$fields{"nicknamemessage"} = "nickname name already exists, please choose again!";
        ptHTML::displayHTML("../html/join.html", %fields);
	    }
    else
        {
        # if its not, add it to the database.
        $list{$fields{"nickname"}} = 1;
        # mayaswell store all the information in here aswell.
        $list{$fields{"nickname"} . "name"}        = $fields{"name"};
        $list{$fields{"nickname"} . "email"}       = $fields{"email"};
        $list{$fields{"nickname"} . "website"}     = $fields{"website"};
        $fields{"mods"} =~ s/\n/~/g; # replace CR with ~
        $list{$fields{"nickname"} . "mods"}        = $fields{"mods"};
        $fields{"comment"} =~ s/\n/~/g; # replace CR with ~
        $list{$fields{"nickname"} . "comment"}     = $fields{"comment"};
        $list{$fields{"nickname"} . "car"}     = $fields{"car"};
        $list{$fields{"nickname"} . "password"}    = $fields{"password"};
        $list{$fields{"nickname"} . "picture1"}    = $fields{"picture1"};
        $list{$fields{"nickname"} . "picture2"}    = $fields{"picture2"};
        $list{$fields{"nickname"} . "picture3"}    = $fields{"picture3"};
        $list{$fields{"nickname"} . "picture4"}    = $fields{"picture4"};
        $list{$fields{"nickname"} . "picture5"}    = $fields{"picture5"};
        $list{$fields{"nickname"} . "picture6"}    = $fields{"picture6"};
        $list{$fields{"nickname"} . "dontshow"}    = $fields{"dontshow"};

        $fields{"memberlink"} = "<A HREF='http://www.ftowa.com/cgi-bin/showprofile.cgi?member=" . $fields{"nickname"} . "'>profile page</A>";

        # make a member folder.. this will contain the pix
        $name = $fields{"nickname"};
        # create Member dir
#    	if ( ! ( -e "../profiles/$name" ) )
#    		{
#        	mkdir ("../profiles/$name", 0750) or die("Error Creating Member Directory");
#            }

        # save the members flat file.
        &ptDIO::saveFile("members", %list);

        # send an email.
#        &ptDIO::sendEmail($fields{"email"}, "FTO Drivers Club (www.ftowa.com)",
#                          "Welcome to the FTO Drivers Club",
#                          "Welcome " . $fields{"name"} , ",\n\n" ,
#                          "You have tapped into the central source of local FTO information for Perth," ,
#                          "Western Australia.  You will receive regular email updates informing you of " ,
#                          "event and cruise information, aswell as access to local technical articles so " ,
#                          "you can better choose your source of FTO parts and services.\n\n" ,
#                          "We are using the JCars Messageboard as our central messaging service for general " ,
#                          "FTO related discussion. JCars contains a wealth of searchable knowledge and lots " ,
#                          "of people who have experienced almost all possible obstables involved with ownership " ,
#                          "of the FTO in general. If you have a problem, someone on there will be able to point " ,
#                          "you in right direction.\n\n" ,
#                          "Please look around the website, look at your profile (in the community section of the " ,
#                          "website). All our events and cruises will be documented and photographed on these " ,
#                          "pages.\n\n" ,
#                          "Stickers will be available (One size only, 200mm * 28mm) for purchase and are decal " ,
#                          "style, suitable for rear windscreen or paintwork. The cost of these stickers will be $1.50" ,
#                          "which is actually cost price!! If you wish to get ahold of a sticker at the next meeting " ,
#                          "then email me (Mark) and I will bring one along for you. If you are interested in a larger " ,
#                          "sticker ala some of the other car clubs cruising around we can organise these " ,
#                          "stickers sized at 600mm * 200mm. The price for these is subject to change but the " ,
#                          "quote for quantities of 10 is $6.50 each.\n\n" ,
#                          "For your personal information:\n" ,
#                          "Your User name: " , $fields{"nickname"} , "\n" ,
#                          "Your Password: " ,  $fields{"password"} , "\n\n" ,
#                          "Thanks for joining us, we will be in contact soon, \n\n" ,
#                          "Mark Allanson (marke@ftowa.com)");

        # everythign is fine, display the success message
        ptHTML::displayHTML("../html/joinThanks.html", %fields);

        }

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