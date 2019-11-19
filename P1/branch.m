function value = branch(N, d)


v = ones(1, d+1);
v(end) = -N;

p = roots(v);

p(end);

value = p(end);

end