# breversals.pl  
#
# DG Sept. 14, 2017
#
# This creates the  compact ILP for sorting-by-reversals problem. The first permutation is assumed to be
# the identity permutation, i.e., the integers from 1 to n in natural order. So the input only specifies the second permutation,
# i.e., P2. 
# The ILP formulation is the one detailed in Lancia et al paper. Note that 
# the X variables are the
# driving variables, not the R variables. 
#
# This is the version discussed in ``Integer Programming in Computational and Systems Biology".
#
#
# The X variable has four parameters: level, origin of flow from level 1 (i.e., the integer), node at level, node at level+1. 
# So this is a ``flow out" variable.
#
# The R variable has three parameters: left, right, level. So R(i,j,k) means that there is a rotation between positions
# i and j > i at level k.
#
# Call the program on a command line in a terminal window as:
# perl breversals.pl number file-name

# where ``number" is n, the number of integers in the permutation, and ``file-name" is the name of the file where
# permutation P2 is written on one line. The ILP formulation is output to a file whose name begins with the letter `R', followed
# by the input file-name, followed by `.lp'.
#
# The ILP formulation created will be in a file named Rfile-name.lp

$n = $ARGV[0]; # number of elements, numbered 1 through $n.
$nm1 = $n - 1;
open (IN, "$ARGV[1]"); # file where the permutation is.
open (OUT, ">R$ARGV[1].lp");

$perm = <IN>;
chomp $perm;
@pi = split (' ', $perm);
# print "@pi \n";

# compute the lower bound based on breakpoints
$ls = 0;
if ($pi[0] != 1) {
   $ls++;
}
if ($pi[$n-1] != $n) {
   $ls++;
}

foreach $i (1 .. $n-1) {
  if (abs ($pi[$i] - $pi[$i-1]) != 1) {
     $ls++;
  }
}
$lb = int ($ls/2 + 0.6);

%bin = ();
$Rlist = "";   # list of all the possible Reversal operations
%Rlistk = ();  # hash with key k: string with all the possible Reversal operations at level k
$start = "";
$finish = "";
$forbidout = "";
$forbidin = "";
$RX = "";
%Rmissw = (); # hash with key w,k: string with all Reversal operations at level k that don't move w

foreach $k (1 .. $n-1) {  # initialize Rlistk
     $Rlistk{$k} = "";
}

foreach $w (1 .. $n) {   # initialize Rmissw. Rmissw{w,k} lists all of the rotations that don't change position w at level k
   foreach $k (1 .. $n) {
     $Rmissw{$w,$k} = "";
   }
}

 foreach $i (1 .. $n) { #1
#    $pi[$i] = $i + 1;  # this makes the right shift permutation - a simple permutation used for debugging.
#    $pi[$n] = 1;

    foreach $j (1 .. $n) { #2
        foreach $a (1 .. $n) { #3 
           if ($a == $i) { #4
                 $start .= "+ X(1,$i,$a,$j) "; # at level 1 the only level moves for the origin i element is i to j
                 $bin{"X(1,$i,$i,$j)"} = 1;
           } #4
           else { #4
                $forbidout .= "+ X(1,$i,$a,$j) "; # all other moves for the origin i element at level 1 are forbidden
           } #4
           if ($i == $pi[$a-1]) { #4
                   $finish .= "+ X($nm1,$i,$j,$a) "; # at level n-1 the only moves for the origin i element is to pi[i]
                   $bin{"X($nm1,$i,$j,$pi[$i-1])"} = 1;
           } #4
           else { #4
                $forbidin .= "+ X($nm1,$i,$j,$a) ";  # all other moves for the origin i element at level n-1 are forbidden
           } #4
    } #3

        foreach $k (1 .. $n-1) { #3
           if ($j > $i) { #4
              $Rlistk{$k}  .= "+ R($i,$j,$k) "; # accumulate the possible Reversals at level k, with i < j
              $Rlist  .= "+ R($i,$j,$k) ";
              $bin{"R($i,$j,$k)"} = 1; 
#              print "R $i $j $k \n";


             foreach $w (1 .. $n) { #5 # acculate most of the reversals at level k that don't change the integer at position w.
                if ((($i < $w) and ($j < $w)) or (($i > $w) and ($j > $w))) { #6  w is outside the rotation intervals
                    $key = $w . ',' . $k;
#                    print "key:  $key \n";
                    $Rmissw{$key} .= "- R($i,$j,$k) ";
                } #6
             } #5
           } #4

#        foreach $kley (sort keys %Rmissw) {
#             print "$kley  $Rmissw{$kley}\n";
#        }

#          $kp1 = $k + 1;
#          $jp1 = $j + 1;
       } #3
    } #2
    $start .= " = 1\n";
    $finish .= " = 1\n";
    $forbidout .= " = 0\n";
    $forbidin .= " = 0\n";
} #1 
          
print OUT "Minimize \n S \n\n Such that \n\n";
print OUT "$Rlist - S = 0 \n\n ";
print OUT "S >= $lb \n";

print OUT "$start\n";
 print OUT "$forbidout\n";
print OUT "$finish\n";
 print OUT "$forbidin\n";

foreach $k (2 .. $n-1) { #1  for each k from 2 to n-1, if integer i flows into j at level k,
                         # then integer i must flow out of j to level k+1 
     $km1 = $k - 1; 
     foreach $i (1 .. $n) { #2
          foreach $j (1 .. $n) { #3
              $inkij = "";
              $outkij = "";
              foreach $a (1 .. $n) { #4
                 $inkij .= "+ X($km1,$i,$a,$j) ";
                 $bin{"X($km1,$i,$a,$j)"} = 1;
              } #4
              foreach $a (1 .. $n) { #4
                 $outkij .= "- X($k,$i,$j,$a) ";
                 $bin{"X($k,$i,$j,$a)"} = 1;
              } #4
              if (! defined $collectin{"$km1,$j"}) { #4 collect all of the inkij strings to j from level k - 1.
                      $collectin{"$km1,$j"} = $inkij;
              } #4
              else { #4
                      $collectin{"$km1,$j"} .= $inkij;
                    } #4

              print OUT "$inkij $outkij = 0 \n"; # flow in of an integer i to node j at level k must equal flow
                                                   # out.
#              print "$k, $i, $j \n";
          } #3
     } #2
} #1
print OUT "\n";

#$intokj = ""; # new block Sept. 26, 2017  generate inequalities to require that
#foreach $k (1 .. $n-1) { # there is exactly one flow into each node at levels 2 through n
                          # This should not be needed, but can't hurt.
#  foreach $j (1 .. $n) {
#     foreach $a (1 .. $n) {
#       foreach $i (1 .. $n) {
#          $intokj .= "+ X($k,$i,$a,$j) ";
#       }
#      }
#      print OUT "$intokj = 1 \n";
#      $intokj = "";
#   }
#}


foreach $k (1 .. $n-1) {  # there must be exactly one operation at any level k from 1 through n-1
    print OUT "$Rlistk{$k} + NOP$k = 1 \n\n";
}
print OUT "\n";

foreach $key (sort keys %collectin) { #1
             print OUT "$collectin{$key} <= 1\n"; # there is at most one flow to node j at level k
} #1       
print OUT "\n";

foreach $k (1 .. $n-1) { #1   # now connect the X variables to the R variables.
    foreach $a (1 .. $n) { #2 edge from node a at level k to node j at level k+1
       foreach $j (1 .. $n) { #3
          $edgeset = "";
          foreach $i (1 .. $n) { #4 enumerate the integers
             $edgeset .= "+ X($k,$i,$a,$j) "; # enumerate all possible X variables
          } #4
          print OUT "$edgeset \n"; # k, a and j are fixed here, and i varies in the edgeset.
#          print OUT " sum of negation of every R(k,x,y) that moves an integer from $a to $j at level $k\n";

          if ($a == $j) { #4  flowing from and to the same positions in levels k-1 and k.
             $string = "$a,$k";
#             print "YES $Rmissw{$string} \n";
#             print OUT "- NOP$k "; # this is consistent with what Lancia uses, but I get that the problem
                                    # is infeasible when I used just this, rather than the next line.
#
             print OUT "- NOP$k  $Rmissw{$string}"; # all the ways that the integer at position $a at level k is
                                                    # the same as at level k+1
                                                    # Lancia does not use this, and logically 
                                                    # it seems it is not needed. It
                                                    # is subtle. It may be hard for students to understand this.
                                                    # And, the problems end up infeasible without it. I am not
                                                    # sure why.
          } #4

          if ($a < $j) { #4 
             $l = $a;
             $r = $j;
          } #4
          else { #4
             $l = $j;
             $r = $a;
          } #4
            
          if (($l - 1) < ($n - $r)) { #4 find which (out)side of the interval between a and j 
                                      # is smallest. The left side
                                      # has length l-1, and the right side has length n - r.
             $b = $l-1;
          } #4
          else { #4
             $b = $n - $r;
          } #4
#          print OUT "The bound is $b \n";
         
          foreach $w (0 .. $b) { #4  enumerate rotations that result in a flow from node a (level k) to 
                                 #   node j (level k+1).
             $bl = $l - $w;
             $br = $r + $w;
             if ($bl != $br) { #5
                 print OUT "- R($bl,$br,$k) ";
             } #5
          } #4
          print OUT "<= 0 \n\n";
       } #3
    } #2
} #1
foreach $i (1 .. $n-2) { #1
        $ip1 = $i + 1;
        print OUT "NOP$i - NOP$ip1 <= 0\n";  # if a NOP is used at level i, it must be used at all suceeding levels.
        $bin{"NOP$i"} = 1;
} #1
$nm1 = $n-1;
$bin{"NOP$nm1"} = 1;

print OUT "binaries \n";
foreach $var (sort keys %bin) { #1
     print OUT "$var \n";
} #1


print OUT "end";

print "The ILP file is R$ARGV[1].lp \n";
