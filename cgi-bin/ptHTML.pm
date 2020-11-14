package ptHTML;

sub startHTML #()
	{
	print("Content-type: text/html\n\n");
	}


sub startText #()
	{
	print("Content-type: text/plain\n\n");
	}

sub tHTML #(filename)
	{
	my ($fileName)	= @_;
	my $root 		= $ENV{"DOCUMENT_ROOT"};

    return "$root/html/thtml/$fileName";
	}

sub validEmail #(email)
	{
	my ($email) = @_;
	return ($email =~ m/.+@.+\..+/);
	}



# Template HTML is our scripting style language that replaces anything in
# a HTML file between ~ charaters with a corresponding value within a
# supplied hash table. used for adding database information to HTML files
# without having to use PHP etc.
sub displayHTML #(fileName, %data)
	{
	my ($fileName, %data)		= @_;
	my $line;

    if (open(FILE, "<$fileName")) {
		while($line = <FILE>) {
			while ($line =~ s/~([^ ]+)~/$data{$1}/e) { };
			print $line;
		}
        close(FILE);
    }

	}

1;