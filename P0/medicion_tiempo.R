library(pryr)

M = function(n) {k = 2^n; return(matrix(runif(k*k), nrow = k))}

for (n in 5:10) 
{
cat('La matriz', n, 'con', 2^n, 'elementos tarda',
system.time(M(n))[3], 'segundos en crearse y pesa', object_size(M(n)), 'bytes', '\n')
}
