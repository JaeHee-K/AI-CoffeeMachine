import numpy as np
import math

csvdata = np.loadtxt("unsuper_coffee.csv", delimiter=",", encoding='utf-8-sig')
#x, y = csvdata.shape
print(csvdata.shape)
x = 1000
y = 2


###변수 정의###
GAMMAR = 1.0
K = 0.5
ii = 1
output_neuron = np.zeros(10)
m_cluster = 0
m_datanum = 1000
m_datanum2 = 1
cluster_centroid = np.zeros((1000,4))
winner = 0
m_TAU = 4.0  #4.0
m_fK = 1.0

global m_number2
m_number = 1
m_number2 = 1 #n번째 회전
m_round = 1

#오버플로 방지를 위한 뮤 확인
fuzzy_member = np.zeros(10) # 뮤(u) 값
membership_value = 0.0

#||X-V||e^-u <= T가 되는지 확인
vigilance_constant = 0.0
vigilance_test_result = ''

#들어온 데이터 값에 맞는 클러스터가 없을 경우
def first_cluster():
    global winner
    winner = 1
    global output_neuron
    output_neuron[1] = 1
    global m_cluster
    m_cluster += 1
    global cluster_centroid

    for k in range(m_datanum2):
        cluster_centroid[k][1] = data[k]

#들어온 데이터 값에 맞는 클러스터를 찾는 부분
def test_cluster():
    win_dist = np.zeros((y,20))
    square_win_dist = np.zeros((y,20))
    square_win_distance = np.zeros(20)
    de_win_distance = np.zeros(20)
    short_distance = 0.0
    exp_const = 0.0
    global membership_value
    global vigilance_constant
    global vigilance_test_result
    global cluster_centroid

    for i in range(20):
        square_win_distance[i] = 0.0

    win_distance = np.zeros(20)
    for i in range(1, m_cluster+1):
        for k in range(m_datanum2):
            win_dist[k][i] = data[k] - cluster_centroid[k][i]
        for k in range(m_datanum2):
            square_win_dist[k][i] = win_dist[k][i]*win_dist[k][i]
        for k in range(m_datanum2):
            square_win_distance[i] += square_win_dist[k][i]
        win_distance[i] = np.double(square_win_distance[i])
        de_win_distance[i] = np.float(math.sqrt(win_distance[i]))

    #초기 winner=1
    global winner
    global fuzzy_member
    winner = 1
    short_distance = de_win_distance[1]
    #membership_value = 3.0
    #클러스터의 개수가 2개 이상일 때
    #클러스터간 경쟁을 통하여 승자를 결정하고 vigilance test를 한다
    for i in range(2, m_cluster+1):
        if short_distance > de_win_distance[i]:
            winner = i
            short_distance = de_win_distance[i]

    for i in range(1, m_cluster+1):
        fuzzy_member[i] = 0.0
    #유클리디안 거리가 같을 때
    if short_distance == 0.0:
        fuzzy_member[winner] = 1.0
        membership_value = 1.0
    else:
        membership()

    #GAMMAR = 1
    if m_cluster >= 2:
        exp_const = float(-(GAMMAR*membership_value))
        vigilance_constant = float(math.exp(exp_const))
        vigilance_test()
    elif m_cluster == 1:
        vigilance_constant = float(math.exp(0.0))
        vigilance_test()

    if vigilance_test_result == 'Y':
        commit_cluster()
    else:
        uncommit_cluster() #만족스러운 군집이 없으면 새로운 클러스터 생성

def membership():
    distance = np.zeros((y,20))
    square_distance1 = np.zeros((y,20))
    square_distance = np.zeros(20)
    inverse_s_distance = np.zeros(20)
    inverse_distance = 0.0
    global membership_value
    global fuzzy_member

    for i in range(20):
        square_distance[i] = 0.0
    for i in range(1, m_cluster+1):
        for k in range(m_datanum2):
            distance[k][i] = data[k] - cluster_centroid[k][i]
        for k in range(m_datanum2):
            square_distance1[k][i] = distance[k][i]*distance[k][i]
        for k in range(m_datanum2):
            square_distance[i] += square_distance1[k][i]
        inverse_s_distance[i] = 1/square_distance[i]

    for i in range(1, m_cluster+1):
        inverse_distance = inverse_distance + inverse_s_distance[i]

    for i in range(1, m_cluster+1):
        fuzzy_member[i] = inverse_s_distance[i]/inverse_distance

    membership_value = inverse_s_distance[winner]/inverse_distance

def vigilance_test():
    distance_winner1 = np.zeros(y)
    s_distance_winner = 0.0
    fuzzy_distance = 0.0
    distance_winner = 0.0
    temp = 0.0
    global vigilance_test_result
    for k in range(m_datanum2):
        distance_winner1[k] = data[k] - cluster_centroid[k][winner]
    for k in range(m_datanum2):
        temp = distance_winner1[k]*distance_winner1[k]
        s_distance_winner += temp

    distance_winner = math.sqrt(float(s_distance_winner))
    fuzzy_distance = float(distance_winner*vigilance_constant)

    if m_cluster == 1:
        if distance_winner <= m_TAU:
            vigilance_test_result = 'Y'
        else:
            vigilance_test_result = 'N'
    else:
        if fuzzy_distance <= m_TAU:
            vigilance_test_result = 'Y'
        else:
            vigilance_test_result = 'N'

def commit_cluster():
    winner_distance1 = np.zeros(y)
    s_winner_distance1 = np.zeros(y)
    s_winner_distance = 0.0
    function_iteration = 0.0
    pi_membership_td = 0.0
    pi_membership = np.zeros(20)
    update = np.zeros(20)
    update_fuzzy = np.zeros(20)
    winner_distance = np.zeros(20)
    i = 0
    global output_neuron
    output_neuron[winner] = 1
    global cluster_centroid

    for i in range(1, m_cluster+1):
        #클러스터 개수가 2개 이상일 때
        for k in range(m_datanum2):
            winner_distance1[k] = data[k] - cluster_centroid[k][i]
            s_winner_distance1[k] = winner_distance1[k]*winner_distance1[k]
        s_winner_distance = 0.0
        for k in range(m_datanum2):
            s_winner_distance += s_winner_distance1[k]
        winner_distance[i] = math.sqrt(float(s_winner_distance))
        if winner_distance[i] <= m_TAU/2:
            pi_membership_td = float((winner_distance[i]/m_TAU)*(winner_distance[i]/m_TAU))
            pi_membership[i] = 1 - 2*pi_membership_td
        elif winner_distance[i] <= m_TAU:
            pi_membership_td = float((1 - winner_distance[i]/m_TAU)*(1 - winner_distance[i]/m_TAU))
            pi_membership[i] = 2*pi_membership_td
        else:
            pi_membership[i] = 0.0

    function_iteration = float(1 / (m_fK*(m_number2 -1) + 1))

    for i in range(1, m_cluster+1):
        #클러스터의 개수가 1개일때
        if m_cluster == 1:
            for k in range(m_datanum2):
                cluster_centroid[k][i] = (cluster_centroid[k][i] + data[k])/2
        else:
            update[i] = pi_membership[i]*function_iteration*(fuzzy_member[i]*fuzzy_member[i])
            for k in range(m_datanum2):
                cluster_centroid[k][i] = cluster_centroid[k][i] + update[i]*(data[k] - cluster_centroid[k][i])

def uncommit_cluster():
    global winner
    winner = winner + 1
    global m_cluster
    m_cluster = m_cluster + 1
    global output_neuron
    output_neuron[m_cluster] = 1
    global cluster_centroid

    for k in range(m_datanum2):
        cluster_centroid[k][m_cluster] = data[k]

global data
data = csvdata[0:1] # x축은 0번째 요소, y축은 4개의 요소
first_cluster()


for i in range(1, x):
    data = csvdata[i:i+1]
    test_cluster()
m_number2 += 1

winner1_1 = 0
winner1_2 = 0
winner1_3 = 0
winner2_1 = 0
winner2_2 = 0
winner2_3 = 0
winner3_1 = 0
winner3_2 = 0
winner3_3 = 0
count = 0
error1 = 0
error2 = 0

for j in range(0,1):
    for i in range(0, x):
        data = csvdata[i:i+1]
        test_cluster()
        if j == 49:
            print(count+1, "번째 :", winner)
            count += 1
            if count == 1000:
                count = 0

            if winner == 2:
                if data >= 6:
                    error1 += 1
            elif winner == 1:
                if data <= 5:
                    error2 += 1

    m_number2 += 1

print("\n\n\n=====================결과=====================")
print("총 클러스터 개수 : ", m_cluster)
for i in range(1, m_cluster+1):
    print(i, "번째 클러스터의 대표 값 : ", end=" ")
    for j in range(m_datanum2):
        print(round(cluster_centroid[j][i],2), end=" ")
    print("")
print("winner 1 error :", error1)
print("winner 2 error :", error2)
print("==============================================")

# Start Test
testdata = np.loadtxt("super_coffee_test.csv", delimiter=",", encoding='utf-8-sig')
class1count = 0
class2count = 0
for i in range(0, x):
    data = testdata[i:i+1]
    class1 = cluster_centroid[0][1] - data
    class2 = cluster_centroid[0][2] - data
    if abs(class1) < abs(class2):
        class1count += 1
    elif abs(class1) > abs(class2):
        class2count += 1

print("Supervised Test")
print("Supervised class 1 :",class1count)
print("Supervised class 2 :",class2count)
print("==============================================")