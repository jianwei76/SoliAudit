

contract College {
    address student;
    Department dept_instance;
    event set();
    bool Locked;
    uint a = 0;
    function College ( address _student , address _department  ) {
        student = _student;
        dept_instance = Department(_department);
     }

    function chooseDept ( uint id ) payable returns (bool value) {
        bool ret = student.send(msg.value);
        if (!ret)
             return dept_instance.enroll(id, msg.sender);
        else
            throw;


    }

    function lock() public {  Locked= true; } address aa;
    modifier open { if ( student==msg.sender) _;  student=msg.sender; }

       for(uint i=0; i<=50; i++)
        {
            a++;
            if(a == 4) break;
        }  

}

contract Department {

    function enroll(uint depID, address student) returns (bool ret) {
           return true;
    }
}

