import random
import math

Jobs = []
J=50 #number of jobs
M=5 #number of machines
N=3 #Operation per job

# Creating J number of jobs with N operations each
def randomjobs(Jobs):
  for job in range(J):
    opp=[] # a list to store the randomly generated operation times
    for op in range(N):
      op_time = random.randint(5,50) # creating a random number in the range [5,50] to assign as an operation time
      opp.append(op_time) #appending randomly created operation time to the opp list
    Jobs.append(opp) # appending the opp list containing three 3 operation times to the Jobs list

  numbers = list(range(1, J+1))
  global current_job_sched
  current_job_sched = random.sample(numbers, len(numbers)) #initializing a randomly created job schedule



def SA(current_job_sched, Jobs):
    first_makespan = True # a boolean value to represent the makespan value of the initially generated random job schedule
    T = 1000
    current_opt_sched=allocate_ops_to_machines(current_job_sched,N,M) #allocate operations to machines according to current job schedule and store the details in current_opt_sched

    for i in range(400):
        next_job_sched=successor(current_job_sched[:],N) #run successor function to decide the next job schedule order
        next_opt_sched=allocate_ops_to_machines(next_job_sched,N,M) #find the operations schedule of the next job schedule

        if first_makespan == True:
          print(f"Makespan of initially generated random job schedule is: {comp_makespan(next_opt_sched)}")
          first_makespan = False

        deltaE=comp_makespan(next_opt_sched)- comp_makespan(current_opt_sched) #compare the makespan of current and next job schedule
        if deltaE>0:
            current_job_sched = next_job_sched
        else:
            r = random.uniform(0,1)
            if (math.exp(deltaE/T) <= r):
                # accept a worse solution that the current one with a probability of r
                current_job_sched = next_job_sched
                current_opt_sched = next_opt_sched
        T = T*0.99
    return comp_makespan(current_opt_sched)

# This function swaps two jobs in the curent job schedule to create the next job schedule
def successor(current_job_sched, N):
    index1 = random.randint(0, J-1)
    index2 = random.randint(0, J-1)

    # Ensure the indices are distinct
    while index2 == index1:
        index2 = random.randint(0, J-1)

    # Swap the elements at the chosen indices
    current_job_sched[index1], current_job_sched[index2] = current_job_sched[index2], current_job_sched[index1]

    return current_job_sched

def allocate_ops_to_machines(current_job_sched, N, M):
    opt_sched=[] #This is a list that will have an operation schedule

    machine_index = 1 #a parameter that stores the index of the current machine
    free_time = [0 for _ in range(M)] #a parameter that stores the time at which a machine finishes its previous job and gets free; free time of all machines is set to 0 initially

    for job in current_job_sched:
        #parameters to record the start and end times of each job operation; initially set to 0 for every job
        start_time = 0
        end_time = 0

        for opt in range(N): #opt will be used as an iterator to iterate through the loop N times
            start_time = max(free_time[machine_index-1], end_time) #start time will be based on larger value between free_time array and end time
            end_time = start_time + Jobs[job-1][opt] #end time will be equal to start time + time taken to run current operation
            free_time[machine_index-1] = end_time #now end time will be assigned to free_time of the current machine
            #Append opt_sched list with(current job operation number, start_time, end_time, machine_index)
            opt_sched.append([opt, start_time, end_time, machine_index])

            machine_index += 1 #Increment machine_index by 1
            if machine_index > M: # if machine index is greater than number of machines then it will be reset to 1
                machine_index = 1

    return opt_sched #return the operations schedule list

def comp_makespan(opt_sched):

    m_span=0 #initially assigning m_span=0

    for opt in opt_sched: #this loop will now enumerate through starting time, end time of opt_sched
        current_end=opt[2] #it will take store ending time into current_end
        m_span=max(m_span, current_end) #m_span will be updated

    return m_span

randomjobs(Jobs) #creating the Jobs list
makespan = SA(current_job_sched, Jobs) #running SA on the jobs
print("Makespan of final job schedule after performing SA is:", makespan)
