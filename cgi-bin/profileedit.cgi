#!C:\Perl\bin\perl.exe

use CGI qw(:standard);
use ptHTML;
use ptDIO;

&ptHTML::startHTML();

$|     = 1;
$nickname = $ENV{"REMOTE_USER"};

$params    = &loadParameters();

if  ((!$params) or
    (($fields{"name"} eq "") or ($fields{"email"} eq "")))
    {

    %list = &ptDIO::loadFile("members");

    # load all the informatiuo9n for this member out of our hash

    $fields{"name"}     = $list{$fields{"member"} . "name"};
    $fields{"email"}    = $list{$fields{"member"} . "email"};
    $fields{"website"}  = $list{$fields{"member"} . "website"};
    $list{$fields{"member"} . "mods"} =~ s/~/\n/g; #replace tilde with CR
    $fields{"mods"}     = $list{$fields{"member"} . "mods"};
    $list{$fields{"member"} . "comment"} =~ s/~/\n/g; #replace tilde with CR
    $fields{"comment"}  = $list{$fields{"member"} . "comment"};
    $fields{"car"}      = $list{$fields{"member"} . "car"};
    $fields{"picture1"} = $list{$fields{"member"} . "picture1"};
    $fields{"picture2"} = $list{$fields{"member"} . "picture2"};
    $fields{"picture3"} = $list{$fields{"member"} . "picture3"};
    $fields{"picture4"} = $list{$fields{"member"} . "picture4"};
    $fields{"picture5"} = $list{$fields{"member"} . "picture5"};
    $fields{"picture6"} = $list{$fields{"member"} . "picture6"};
    $fields{"dontshow"} = $list{$fields{"member"} . "dontshow"};

    if ($list{$fields{"member"} . "dontshow"})
        {
            $fields{"dontshowchecked"} = "CHECKED";
        }

    ptHTML::displayHTML("../html/memberdetailsedit.html", %fields);

    }

# SAVE THE NEW DATA
else
    {

    %list = &ptDIO::loadFile("members");

    # make sure the passwords match

    if ($fields{"password"} ne $list{$fields{"member"} . "password"})
        {
        ptHTML::displayHTML("../html/badpassword.html", %fields);
        }
    else
        {
        # update the details in the database
        $list{$fields{"member"}} = 1;
        # mayaswell store all the information in here aswell.
        $list{$fields{"member"} . "name"}       = $fields{"name"};
        $list{$fields{"member"} . "email"}       = $fields{"email"};
        $list{$fields{"member"} . "website"}     = $fields{"website"};
        $fields{"mods"} =~ s/\n/~/g; # replace ~ with CR
        $list{$fields{"member"} . "mods"}        = $fields{"mods"};
        $fields{"comment"} =~ s/\n/~/g; # replace ~ with CR
        $list{$fields{"member"} . "comment"}     = $fields{"comment"};
        $list{$fields{"member"} . "car"}     = $fields{"car"};

        $list{$fields{"member"} . "picture1"}    = $fields{"picture1"};
        $list{$fields{"member"} . "picture2"}    = $fields{"picture2"};
        $list{$fields{"member"} . "picture3"}    = $fields{"picture3"};
        $list{$fields{"member"} . "picture4"}    = $fields{"picture4"};
        $list{$fields{"member"} . "picture5"}    = $fields{"picture5"};
        $list{$fields{"member"} . "picture6"}    = $fields{"picture6"};
        $list{$fields{"member"} . "dontshow"}    = $fields{"dontshow"};

    #    print "Details should be saved";

        # save the members flat file.
        &ptDIO::saveFile("members", %list);

        &ptHTML::displayHTML("../html/updatesuccess.html", %fields);
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