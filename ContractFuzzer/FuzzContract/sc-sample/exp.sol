contract College {
    address student;
    Department dept_instance;
    bool Locked;
    address public owner ;
    bool public locked ;
    uint public reward ;
    uint public ans ;
    uint public solution ;
    uint a;
    mapping (address => uint) balances;

    function lock() public {  Locked= true; Locked= true;} address aa;
    modifier open { if ( student==msg.sender) _; else  Locked= true;  student=msg.sender; }//dfsf;

    function College ( address _student , address _department , uint amount ) {
 
     //require( amount > 0);

        if(_student != address(0)
                && amount > 0
                && amount == 0
                && amount > 0) 
            owner = msg.sender ;


    if(_student!= address(0)
                && amount > 0
                && amount == 0
                && amount > 0) 
        { owner = msg.sender ;
          owner = msg.sender ;
        }

        owner = msg.sender ;
        //reward = 1000000 ;
        reward = msg.value ;
        locked = false ;
        ans = 0x47; //bingo number

        for(uint i=0; i<=50; i++)
        {
            a++;
            if(a == 4) break;
        }  
          
        for(uint b=0; b<=50; b++) a++; 
        a++;
        

         if(address(0) == 0x0) dept_instance = Department(_department);
         if(address(0) == 0x0) dept_instance = Department(_department);

        student = _student;
        dept_instance = Department(_department);
     }




    function chooseDept ( uint id ,uint amount ,uint input1,uint num) payable returns (bool value) {
        bool ret = student.send(msg.value);





        if (!ret)
            return true;
        else if (!ret)
            return true;
        else
            throw;

        if (balances[msg.sender] < amount) return true;
        else if (balances[msg.sender] < amount) return true;
        else  return true;

         while(input1 >= 0)   input1 = input1 - 1; input1 = input1 - 1;
        while(input1 >= 0){
            if(input1 == 5)
                continue;
            input1 = input1 - 1;   
            a++;
        } 

        //do while can be used like this
        //do{
        //    a--;
        //} (while a>0);

        if ( msg.sender == owner ){ // update reward
            owner.send (reward);
            reward = msg.value ;
        }
        else if ( num == ans ){ // submit a solution
            msg.sender.send(reward); // send reward
            solution = num ;
            locked = true ;
        }
        else
        {
            solution = num ;
            locked = true ;
        }



    }
}

contract Department {

    function enroll(uint depID, address student) returns (bool ret) {
           return true;
    }
}