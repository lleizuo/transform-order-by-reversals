# transform-order-by-reversals
For integer linear proramming, there are following formulas:  
#####1 One operation or NO-OP. One and only one is 1.
<img src="https://latex.codecogs.com/svg.latex?\Large&space;NOP(k) + \sum_{(p,q):p<q}R(p,q,k) = 1" title="\Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" />
#####2 Each integer flows to somewhere at level one. One and only one is 1.
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\sum_{q=1}^{n}X(1,i,i,q) = 1" title="\Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" />
#####3 Each integer is in its postion at level n. One and only one is 1.
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\sum_{p=1}^{n}X(n-1,i,p,Q_2(i)) = 1" title="\Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" />