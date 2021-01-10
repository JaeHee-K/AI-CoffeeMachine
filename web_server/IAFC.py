import numpy as np
import math

# first CSV file read
csvdata = np.loadtxt("iris.csv", delimiter=",", encoding='utf-8-sig')
x, y = csvdata.shape
# slicing data into x and y and z
#x = csvdata[:,:4]    # 모든 행, 마지막을 제외한 모든 열
#y = csvdata[:,[-1]]    # 모든 행, 마지막 열

###변수 정의###
GAMMAR = 1.0
K = 0.5
ii = 1
output_neuron = np.zeros(10)
m_cluster = 0 #테스트 용으로 정수 변경, 원래 0으로 초기화
m_datanum = 150
m_datanum2 = 4
cluster_centroid = np.zeros((x,y))
winner = 0
m_TAU = 1.8
m_fK = 1.0

global m_number2
m_number = 1 #n번째 입력 데이터
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

    ##print("<<대표 값>>")
    for k in range(m_datanum2):
        cluster_centroid[k][1] = data[k]
        ##print(cluster_centroid[k][1], end=" ")

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
    """print("test처음")
    for i in range(1, m_cluster+1):
        for j in range(m_datanum2):
            print(cluster_centroid[j][i], end=" ")
    print("\n")"""
    win_distance = np.zeros(20)
    #첫 번째 클러스트를 형성하고 두 번째 데이터가 들어오는 부분
    for i in range(1, m_cluster+1):
        ##print("\n\n<<y1 - x1 또는 y2 - x2>>")
        for k in range(m_datanum2):
            win_dist[k][i] = data[k] - cluster_centroid[k][i]
            ##print(round(win_dist[k][i],1), end=" ")
        ##print("\n\n<<각 거리의 제곱 계산>>")
        for k in range(m_datanum2):
            square_win_dist[k][i] = win_dist[k][i]*win_dist[k][i]
            ##print(round(square_win_dist[k][i],2), end=" ")
        ##print("\n\n<<y1-x1과 y2-x2 제곱 한 것을 더함>>")
        for k in range(m_datanum2):
            square_win_distance[i] += square_win_dist[k][i]
            ##print(round(square_win_distance[i],2), end=" ")
        ##print("\n\n<<해당 거리를 정확히 하기 위해 double 형변환>>")
        win_distance[i] = np.double(square_win_distance[i])
        ##print(round(win_distance[i],2))
        ##print("\n<<위 과정 까지의 결과에 루트씌우기>>")
        de_win_distance[i] = np.float(math.sqrt(win_distance[i]))
        ##print(de_win_distance[i])

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

    """global count
    print(count, "번째 :",winner)
    count += 1
    if count == 150:
        count = 0"""

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

    ##print("\n받아들인 상태 값 : ", vigilance_test_result)
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
    ##print("\n-----뮤 값 구하기-----")
    for i in range(1, m_cluster+1):
        ##print("\n<<거리 계산>>")
        for k in range(m_datanum2):
            distance[k][i] = data[k] - cluster_centroid[k][i]
            ##print(round(distance[k][i],2), end=" ")
        ##print("\n\n<<거리의 제곱 계산>>")
        for k in range(m_datanum2):
            square_distance1[k][i] = distance[k][i]*distance[k][i]
            ##print(round(square_distance1[k][i],2), end=" ")
        ##print("\n\n<<제곱 계산 한 것을 더함>>")
        for k in range(m_datanum2):
            square_distance[i] += square_distance1[k][i]
            ##print(round(square_distance[i],2), end=" ")
        ##print("\n\n<<1/결과>>")
        inverse_s_distance[i] = 1/square_distance[i]
        ##print(inverse_s_distance[i])

    ##print("\n<<inverse_distace + inverse_s_distance>>")
    for i in range(1, m_cluster+1):
        inverse_distance = inverse_distance + inverse_s_distance[i]
        ##print(inverse_distance)

    ##print("\n<<fuzzy_member 구하기>>")
    for i in range(1, m_cluster+1):
        fuzzy_member[i] = inverse_s_distance[i]/inverse_distance
        ##print(fuzzy_member[i])

    ##print("\n<<membership_value 구하기>>")
    membership_value = inverse_s_distance[winner]/inverse_distance
    ##print(membership_value)

def vigilance_test():
    distance_winner1 = np.zeros(y)
    s_distance_winner = 0.0
    fuzzy_distance = 0.0
    distance_winner = 0.0
    temp = 0.0
    global vigilance_test_result
    ##print("\n-----||X-V||e^-u <= T가 되는지 확인------")
    ##print("\n<<거리 winner 찾기 과정1>>")
    for k in range(m_datanum2):
        distance_winner1[k] = data[k] - cluster_centroid[k][winner]
        ##print(round(distance_winner1[k],2), end=" ")
    ##print("\n\n<<거리 winner 찾기 과정2>>")
    for k in range(m_datanum2):
        temp = distance_winner1[k]*distance_winner1[k]
        s_distance_winner += temp
        ##print("temp = ",round(temp,2), ", 거리 winner = ", round(s_distance_winner,2))

    ##print("\n<<최종 distance_winner>>")
    distance_winner = math.sqrt(float(s_distance_winner))
    ##print(distance_winner)
    ##print("\n<<최종 fuzzy_distance>>")
    fuzzy_distance = float(distance_winner*vigilance_constant)
    ##print(fuzzy_distance)

    ##print("\n<<조건이 만족스러운지 확인>>")
    ##print("클러스터 갯수 : ", m_cluster)
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
    ##print("상태 : ",vigilance_test_result)

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

    ##print("\n-----commit_cluster 부분------")
    for i in range(1, m_cluster+1):
        #클러스터 개수가 2개 이상일 때
        ##print("\n<<거리 winner 찾기 과정1>>")
        for k in range(m_datanum2):
            winner_distance1[k] = data[k] - cluster_centroid[k][i]
            s_winner_distance1[k] = winner_distance1[k]*winner_distance1[k]
            ##print("winner_distance1 = ", round(winner_distance1[k], 2), ", s_winner_distance1 = ", round(s_winner_distance1[k], 2))
        s_winner_distance = 0.0
        ##print("\n<<거리 winner 찾기 과정2>>")
        for k in range(m_datanum2):
            s_winner_distance += s_winner_distance1[k]
            ##print(round(s_winner_distance,2), end=" ")
        ##print("\n\n<<최종 승자 거리>>")
        winner_distance[i] = math.sqrt(float(s_winner_distance))
        ##print(winner_distance[i])

        ##print("\n<<최종 승자 거리가 m_TAU/2 보다 작은지, m_TAU보다 작은지 확인>>")
        ##print("- 현재 m_TAU : ", m_TAU,"-")
        if winner_distance[i] <= m_TAU/2:
            ##print("<<최종 승자 거리가 m_TAU/2 보다 작다>>")
            pi_membership_td = float((winner_distance[i]/m_TAU)*(winner_distance[i]/m_TAU))
            pi_membership[i] = 1 - 2*pi_membership_td
        elif winner_distance[i] <= m_TAU:
            ##print("<<최종 승자 거리가 m_TAU보다 작다>>")
            pi_membership_td = float((1 - winner_distance[i]/m_TAU)*(1 - winner_distance[i]/m_TAU))
            pi_membership[i] = 2*pi_membership_td
        else:
            ##print("<<최종 승자 거리가 m_TAU/2, m_TAU보다 크다>>")
            pi_membership[i] = 0.0
        ##print("pi_membership_td : ",pi_membership_td)
        ##print("pi_membership : ",pi_membership[i])

    ##print("\n<<function_iteration 값>>")
    function_iteration = float(1 / (m_fK*(m_number2 -1) + 1))
    ##print(function_iteration)

    # k = 0.5 또는 k = 1.0

    ##print("\n<<클러스터의 대표 값 조정>>")
    for i in range(1, m_cluster+1):
        #클러스터의 개수가 1개일때
        if m_cluster == 1:
            ##print("-현재 클러스터의 개수 1개-")
            ##print("조정 된 대표 값 : ", end="")
            for k in range(m_datanum2):
                cluster_centroid[k][i] = (cluster_centroid[k][i] + data[k])/2
                ##print(round(cluster_centroid[k][i],2), end=" ")
        else:
            ##print("-현재 클러스터의 개수는", m_cluster, "개 이상-")
            ##print("조정 된 대표 값 : ", end="")
            update[i] = pi_membership[i]*function_iteration*(fuzzy_member[i]*fuzzy_member[i])
            ##print("update 값 : ", update[i])
            for k in range(m_datanum2):
                cluster_centroid[k][i] = cluster_centroid[k][i] + update[i]*(data[k] - cluster_centroid[k][i])
                ##print(round(cluster_centroid[k][i], 2), end=" ")

    """print(winner, "번째 클러스터", "바뀐 후")
    for i in range(1, m_cluster+1):
        for k in range(m_datanum2):
            print(cluster_centroid[k][i], end=" ")
    print("\n")"""
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
data = csvdata[0, :y] # x축은 0번째 요소, y축은 4개의 요소
first_cluster()

for i in range(1, x):
    data = csvdata[i, :y]
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

for j in range(0, 50):
    for i in range(0, x):
        data = csvdata[i, :y]
        test_cluster()
        if j == 49:
            print(count, "번째 :", winner)
            count += 1
            if count == 150:
                count = 0
            if i >= 0 and i <= 49:
                if winner == 1:
                    winner1_1 += 1
                elif winner == 2:
                    winner1_2 += 1
                elif winner == 3:
                    winner1_3 += 1
            if i >= 50 and i <= 99:
                if winner == 1:
                    winner2_1 += 1
                elif winner == 2:
                    winner2_2 += 1
                elif winner == 3:
                    winner2_3 += 1
            if i >= 100 and i <= 149:
                if winner == 1:
                    winner3_1 += 1
                elif winner == 2:
                    winner3_2 += 1
                elif winner == 3:
                    winner3_3 += 1
    m_number2 += 1

print("\n\n\n=====================결과=====================")
print("총 클러스터 개수 : ", m_cluster)
for i in range(1, m_cluster+1):
    print(i, "번째 클러스터의 대표 값 : ", end=" ")
    for j in range(m_datanum2):
        print(round(cluster_centroid[j][i],2), end=" ")
    print("")
print("<0~49> winner1 : ",winner1_1," winner2 : ",winner1_2," winner3 : ",winner1_3)
print("<50~99> winner1 : ", winner2_1, " winner2 : ", winner2_2, " winner3 : ", winner2_3)
print("<100~149> winner1 : ", winner3_1, " winner2 : ", winner3_2, " winner3 : ", winner3_3)
print("==============================================")