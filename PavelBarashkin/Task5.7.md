# ### Task 4.7*
# Run the module `modules/mod_a.py`. Check its result. Explain why does this happen.
    5
> After importing mod_c in mod_a module object mod_c will be added in local scope of mod_a. Importing mod_b
> will execute it instructions and redefine variable x in recently added module object mod_c. 

# Try to change x to a list `[1,2,3]`. Explain the result.
    5
> Changing x in mod_c has no effect in mod_a, because mod_b assigns 5 to x, while they both refer 
> to the same module object.

# Try to change import to `from x import *` where x - module names. Explain the result.
    [1, 2, 3]
> In next order:
>               from mod_c import *
>               import mod_b
> Attributes x of mod_c will be copied to the local scope of mod_a before it will change in mod_b.