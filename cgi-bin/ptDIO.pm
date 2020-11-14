package ptDIO;


sub dealersDirectory #() : $dir
    {
    my $root = $ENV{"DOCUMENT_ROOT"};

    return "$root/../dealers"
    }

sub loadFileIntoList #(fileName)
    {
    my ($fileName) = @_;
    my @file       = ();

    if (open(FILE, "<$fileName"))
        {
        @file = <FILE>;
        close(FILE);
        }

    return @file;
    }

sub saveFileIntoList #(fileName, file)
    {
    my ($fileName, @file) = @_;

    if (open(FILE, ">$fileName"))
        {
        print FILE @file;
        close(FILE);
        }
    }


sub loadFile #(fileName)
    {
    my ($fileName)	= @_;
    my %file;
    my $fieldName, fieldValue;
    my $line;

    if (open(FILE, "<$fileName"))
        {
        while($line = <FILE>)
            {
            chomp $line;

            ($fieldName, $fieldValue) = split("=", $line, 2);
            $file{"$fieldName"}       = $fieldValue;
            }

        close(FILE);
        }

    return %file;
    }

sub saveFile #(dealerName, fileName, file)
    {
    my ($fileName, %file) = @_;

    if (open(FILE, ">$fileName"))
        {
        foreach $key (sort(keys(%file)))
            {
            my $value = $file{$key};
            print FILE "$key=$value\n";
    	    }

        close(FILE);
        }
    }




sub sendEmail #($to, $from, $subject, @text)
    {
    my ($to, $from, $subject, @text) = @_;
    my $sendmail                     = "/usr/sbin/sendmail";

    chomp $sendmail;

    # NOTE: For some reason, sendmail fails for all PalmTeq
    #       addresses (eg: randerson@palmteq.com)

    print "<!--";

    if (open MAIL, "|$sendmail -i -t")
        {
        print MAIL "To: $to\n",
                   "From: $from\n",
                   "Subject: $subject\n",
                   "@text\n\n";
        close MAIL;
        }

    print "-->\n";
    }


1;