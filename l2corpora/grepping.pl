
while (<STDIN>) {
  chomp;
  if (m{<selection>([^>]*?)</selection><tag><symbol>WC</symbol><correct>([^<]*?)</correct>}g) {
    print "$1\t\t$2\n";
  }
}
