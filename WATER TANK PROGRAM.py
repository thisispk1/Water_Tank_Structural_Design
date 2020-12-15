import sys

sys.stdin=open('Input.txt','r')
sys.stdout=open('Output.txt','w')

print('#####     Water Tank Design     #####')
print('\n')

L= float(input('Length (in mm)= '))
B= float(input('Breadth (in mm)= '))
H= float(input('Height (in mm)= '))
print('\n')

#SIGMA_cbc
print('-----SIGMA_cbc-----')
M={'M25':8.5,'M30':10,'M35':11.5,'M40':13,'M45':14.5,'M50':16}
SIGMA_cbc=M[(input('Concrete to be used = '))]
print('SIGMA_cbc=',SIGMA_cbc)

#SIGMA_st
print('-----SIGMA_st-----')
SIGMA_st=float(input('SIGMA_st= '))
print('SIGMA_st',SIGMA_st)
print('\n')

#CONSTANTS
print('-----CONSTANTS-----')
M=280/(3*SIGMA_cbc)
print('m=',M)

K=(M*SIGMA_cbc)/(M*SIGMA_cbc+SIGMA_st)
print('k=',K)

J=1-K/3
print('j=',J)

Q=0.5*SIGMA_cbc*K*J
print('Q=',Q)
print('\n')

#THICKNESS OF WALL 
'''TAKING 60mm PER LENGTH in m'''
print('-----THICKNESS OF WALL - TAKING 60mm PER LENGTH in m-----')
THICKNESS=0.06*L
print('Thickness=',THICKNESS)
EFFECTIVE_SPAN=L+(THICKNESS)
print('EFFECTIVE_SPAN=',EFFECTIVE_SPAN)
print('\n')

#MINIMUM AREA OF STEEL
print('-----MINIMUM AREA OF STEEL-----')
Ast_min=(((0.2+((0.1/350)*(450-THICKNESS)))*10*THICKNESS))
print('Ast_min by interpolation=',Ast_min,'mm2')
print('\n')

#L/B Ratio
print('-----L/B Ratio-----')
if L/B < 2:
    h=max(H/4,1000)
    print('Cantilever Action height for the both walls=',h,'mm')
else:
    print('Please choose the dimensions such that L/B ratio is less than 2')
    quit()

print('\n')

#Calculation for x
print('-----Calculation for x-----')
print('Providing cover of 25mm')
Main_Dia=float(input('Diameter of main bar= '))
Distribution_Dia=float(input('Diameter of Distribution bar= '))
d=THICKNESS-25-(Main_Dia/2)
print('d=',d)
x=d-THICKNESS/2
print('x=',x,'mm')
print('\n')

print('-----Contilever Moment-----')
BM=0.5*9.81*H*h*h*0.000000001/3
print('Cantilever moment=',BM,'KNm')
Cantilever_Ast=BM*1000000/(SIGMA_st*J*d)
print('Cantilever Ast=', Cantilever_Ast,'mm2')
if Cantilever_Ast<Ast_min:
    Cantilever_Ast=Ast_min
S_Distribution=3.14*Distribution_Dia*Distribution_Dia*1000/(2*Cantilever_Ast)
print('Provid',Distribution_Dia,'mm bar @',S_Distribution,'mm')
print('\n')

for Z in [L+THICKNESS,B+THICKNESS]:
    if Z==L+THICKNESS:
        print('-----DESIGN FOR LONG WALL-----')
        pass
    else:
        print('-----DESIGN FOR SHORT WALL-----')
        pass

    print('\n')

    #Pull
    print('-----Pull-----')
    P=9.81*(H-h)*0.001
    print('P=',P,'KN/m2')
    Pull_Tl=P*(Z-THICKNESS)*0.001/2
    print('Pull Tl=',Pull_Tl,'KN')
    Pull_Ast=Pull_Tl*1000/SIGMA_st
    print('Pull Ast=',Pull_Ast,'mm2')
    print('\n')

    #Effecive Moment Corner
    print('-----Effecive Moment Corner-----')
    Effective_Corner_Moment=(P*Z*Z*0.000001/12)-(Pull_Tl*x*0.001)
    print('Effective Corner moment=',Effective_Corner_Moment)
    print('\n')

    #Ast for corner moment
    print('-----Ast for corner moment-----')
    Ast_Corner_moment=(Effective_Corner_Moment*1000000)/(SIGMA_st*J*d)
    print('Ast (Corner moment) in mm2=',(Ast_Corner_moment))
    Total_steel_corner=max(Ast_Corner_moment+Pull_Ast,Ast_min)
    print('Total steel corner=',Total_steel_corner,'mm2')
    S_Ast_Corner_moment=3.14*Main_Dia*Main_Dia*1000/(4*Total_steel_corner)
    print('Provide',Main_Dia,'mm bar @',S_Ast_Corner_moment,'mm c/c')
    print('\n')

    #Effecive Moment Midspan
    print('-----Effecive Moment Midspan-----')
    Effective_Midspan_Moment=(P*Z*Z*0.000001/16)-(Pull_Tl*x*0.001)
    print('Effective Midspan moment=',Effective_Midspan_Moment)
    print('\n')

    #Ast for midspan moment
    print('-----Ast for midspan moment-----')
    Ast_Midspan_moment=((Effective_Midspan_Moment*1000000)/(SIGMA_st*J*d))
    print('Ast (Corner moment) in mm2=',Ast_Midspan_moment)
    Total_steel_midspan=max(Ast_Midspan_moment+Pull_Ast,Ast_min)
    S_Ast_Midspan_moment=3.14*Main_Dia*Main_Dia*1000/(4*Total_steel_midspan)
    print('Provide',Main_Dia,'mm bar @',S_Ast_Midspan_moment,'mm c/c')
    print('\n')
print('#####     END     #####')