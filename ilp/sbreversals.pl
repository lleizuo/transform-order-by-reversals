# sbreversals.pl  
#
# DG modify breversals for the signed reversals problem.
# July 23, 2019 - Aug. 1, 2019
#
# This creates the  compact ILP for sorting-by-reversals problem. The first permutation is assumed to be
# the identity permutation, i.e., the integers from 1 to n in natural order, and all signs positive. So the input only specifies the second permutation,
# i.e., P2, and its signs.  
# Note that  the X variables are the  driving variables, not the R variables. 
#
#
# The X variable has four parameters: level, integer, position at the given level, position at the next level, i.e., level+1.
# So X is a essentially a ``flow out" variable. For example, X(2,3,1,5) indicates whether at level 2, integer 3 moves
# from position 1 to position 5. If X(2,3,1,5) is given value 1, then this happens, and if given value 0, then it does not.
#
# The R variable has three parameters: left, right, level. So R(i,j,k) means that there is a reversal between positions
# i and j > i at level k.
#
# The S variable, indicating sign, has two parameters: level, and position. Note that the second parameter
# refers to the position in the list of integers, at the given level. At each level, the permutation at that level, and the list of
# signs are in correct alignment. 
#
# Call the program on a command line in a terminal window as:
# perl breversals.pl number file-name

# where ``number" is n, the number of integers in the permutation, and ``file-name" is the name of the file where
# permutation P2 is written on one line, with spaces between the numbers.
# The second line of the file should have a list of n 0s and 1s. At each position, the sign specifies the sign of the 
# integer aligned with it,  on the first line.

# The ILP formulation is output to a file whose name begins with the letter `SR', followed
# by the input file-name, followed by `.lp'.
# So, for example, if the input file is ``infile", the ILP formulation created will be in a file named SRinfile.lp
#
$n = $ARGV[0]; # number of elements, numbered 1 through $n.
$nm1 = $n - 1;
open (IN, "$ARGV[1]"); # file where the permutation is.
open (OUT, ">SR$ARGV[1].lp");

$perm = <IN>;
chomp $perm;
@pi = split (' ', $perm);
print "@pi \n";


# compute the lower bound, lb, based on the number of breakpoints, ls. This is a bound for the unsigned case, and hence also for the signed
# case. Also, it is known that the number of operations in is at most ls for the unsigned case. 
#
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
$lb = int ($ls/2 + 0.6); # for the signed problem, we should update this to include the signs of neighboring elements in the permutation.

$upprb = $ls + $n; # an upper bound on the number of reversals in the signed case is obtained by first ignoring the signs, reversing to
                      # put the integers in order, and then reversing any individual integer to correct the sign.



%bin = ();
$Rlist = "";   # list of all the possible Reversal operations
%Rlistk = ();  # hash with key k: string with all the possible Reversal operations at level k
$start = "";
$finish = "";
$forbidout = "";
$forbidin = "";
$RX = "";
%Rmissw = (); # hash with key w,k: string with all Reversal operations at level k that don't move w

foreach $k (1 .. $upprb) {  # initialize Rlistk
     $Rlistk{$k} = "";
}

foreach $w (1 .. $n) {   # initialize Rmissw. Rmissw{w,k} lists all of the rotations that don't change position w at level k
   foreach $k (1 .. $upprb + 1) {
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
                   $finish .= "+ X($upprb,$i,$j,$a) "; # at level upprb the only moves for the origin i element is to pi[i]
                   $bin{"X($upprb,$i,$j,$pi[$i-1])"} = 1;
           } #4
           else { #4
                $forbidin .= "+ X($upprb,$i,$j,$a) ";  # all other moves for the origin i element at level upprb are forbidden
           } #4
    } #3

        foreach $k (1 .. $upprb) { #3
           if ($j > $i) { #4
              $Rlistk{$k}  .= "+ R($i,$j,$k) "; # accumulate the possible Reversals at level k, with i < j
              $Rlist  .= "+ R($i,$j,$k) ";
              $bin{"R($i,$j,$k)"} = 1; 
#              print "R $i $j $k \n";


             foreach $w (1 .. $n) { #5 # accumulate most of the reversals at level k that don't change the integer at position w.
                if ((($i < $w) and ($j < $w)) or (($i > $w) and ($j > $w))) { #6  w is outside the rotation intervals
                    $key = $w . ',' . $k;
#                    print "key:  $key \n";
                    $Rmissw{$key} .= "- R($i,$j,$k) ";
                } #6
             } #5
           } #4

#        foreach $kley (sort keys %Rmissw) {  # used for debugging
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

foreach $k (2 .. $upprb) { #1  for each k from 2 to upprb, if integer i flows into j at level k,
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
              print "$k, $i, $j \n";
          } #3
     } #2
} #1
print OUT "\n";


foreach $k (1 .. $upprb) {  # there must be exactly one operation at any level k from 1 through upprb 
    print OUT "$Rlistk{$k} + NOP$k = 1 \n\n";
}
print OUT "\n";

foreach $key (sort keys %collectin) { #1
             print OUT "$collectin{$key} <= 1\n"; # there is at most one flow to node j at level k
} #1       
print OUT "\n";

foreach $k (1 .. $upprb) { #1   # now connect the X variables to the R variables.
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
foreach $i (1 .. $upprb-1) { #1
        $ip1 = $i + 1;
        print OUT "NOP$i - NOP$ip1 <= 0\n";  # if a NOP is used at level i, it must be used at all suceeding levels.
        $bin{"NOP$i"} = 1;
} #1
$bin{"NOP$ls"} = 1;


# Here are the additions to the ILP needed to handle the signed case.

$signconstraints = ""; 
$sign = <IN>; # read the line in the input file that specifying the signs. 
              # Use 0 for negative and 1 for positive. Separate by spaces. A 1 at position $i means that integer $pi[$i] has
              # sign 1 in permutation P2; and similarly for a 0 at position $i. At the first level, the
              # permutation is assumed to be the natural permutation, where all of the integers have sign 1.
              # The signs at the first and last levels are implemented in the ILP by the next code fragment.
chomp $sign;
@signs = split(' ',$sign);
print "@signs \n";
foreach $i (1 .. $n) {
      $upprb1 = $upprb + 1;
      $signconstraints .= "S(1,$i) = 1 \n";   # reverse the right hand sides of the next two equalities to
                                              # modify the program so that it goes from natural order with given signs
                                              # to the input permutation P2 with all positive signs.
      $signconstraints .= "S($upprb1,$i) = $signs[$i-1] \n";
}
print OUT "$signconstraints \n\n";

# Now implement the logic needed for changes in the signs as reversals are made.
$signflip = "";


foreach $l (1 .. $upprb) {      
     foreach $p (1 .. $n) { # Note that in the signed case, we allow the reversal of a single element, which in effect
                            # just changes its sign.
       foreach $q ($p .. $n) {
          foreach $offset (0 .. $q - $p) {
                                         # create the inequalities to implement the logic that if R(p,q,l) is set to 1 (i.e., a rotation
                                         # between p and q at level l is made), then for every position i = p + x that is in that interval at level l,
                                         # the sign for that position in level l+1 will be the reverse of the sign for position j = q - x, from 
                                         # level l. 

             $lp1 = $l + 1;
             $i = $p + $offset;
             $j = $q - $offset;
             $signflip .= "R($p,$q,$l) + S($lp1,$i) + S($l,$j) <= 2 \n";   # if R == 1, then at most one of the Ss can be 1
             $signflip .= "2 R($p,$q,$l) - S($lp1,$i) - S($l,$j) <= 1 \n\n"; # if R == 1, then at least one of the Ss must be 1
             $bin{"S($lp1,$i)"} = 1;
             $bin{"S($l,$i)"} = 1;
          }
         foreach $i (1 .. $p - 1) {  # create the inequalities to implement the logic that if R(p,q,l) is set to 1 then for every position $i before $p, 
                                     # the sign of position $i must be unchanged.
             $signflip .= "R($p,$q,$l) + S($lp1,$i) - S($l,$i) <= 1 \n";   # if R == 1, then S($lp1,$i) = 1 and $S($l,$i) = 0 is excluded.
             $signflip .= "R($p,$q,$l) - S($lp1,$i) + S($l,$i) <= 1 \n";   # if R == 1, then S($lp1,$i) = 0 and $S($l,$i) = 1 is excluded.
                                                                           # So, when R == 1, the two S values must be identical.
         }
         foreach $i ($q+1 .. $n) {  # create the inequalities to implement the logic that if R(p,q,l) is set to 1 then for every position $i after $q, 
                                     # the sign of position $i must be unchanged.
             $signflip .= "R($p,$q,$l) + S($lp1,$i) - S($l,$i) <= 1 \n";   # if R == 1, then S($lp1,$i) = 1 and $S($l,$i) = 0 is excluded.
             $signflip .= "R($p,$q,$l) - S($lp1,$i) + S($l,$i) <= 1 \n";   # if R == 1, then S($lp1,$i) = 0 and $S($l,$i) = 1 is excluded.
                                                                           # So, when R == 1, the two S values must be identical.
         }
      }
   }
     # create the inequalities to implement the logic that if there is a NOP at level l, then the sign at every position at level l+1 must be the
     # same as at level l.
          foreach $i (1 .. $n) {
             $signflip .= "NOP$l + S($lp1,$i) - S($l,$i) <= 1 \n";   # if NOP$l  == 1, then S($lp1,$i) = 1 and $S($l,$i) = 0 is excluded.
             $signflip .= "NOP$l - S($lp1,$i) + S($l,$i) <= 1 \n\n";   # if NOP$l  == 1, then S($lp1,$i) = 0 and $S($l,$i) = 1 is excluded.
                                                                           # So, when NOP$l == 1, the two S values must be identical.
          }
}

# Note that NOP$l + S($l+1,$i) - S($l,$i) <= 0  implements the logic that if the operation at level l is a NOP, then the sign at position i remains unchanged.
# Also, we implement the logic that R($p,$q,$l) = 1, induces a sign change for every position in the [p,q] interval, as
# S($lpq,$p + $offset) = 1 - S($l, $q - $offset). We also implmenet the logic that for any position outside of the interval [p,q],
# the sign doesn't change when doing a [p,q] reversal. In this way, we don't need the ``only if" direction, i.e., that the sign changes at a position i 
# only if i is inside  the interval of reversal, [p,q], at level l.


print OUT "$signflip \n";

print OUT "binaries \n";
foreach $var (sort keys %bin) { #1
     print OUT "$var \n";
} #1


print OUT "end";

print "The ILP file is SR$ARGV[1].lp \n";


