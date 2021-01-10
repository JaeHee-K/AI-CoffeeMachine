import sys
import numpy as np
import math

traindata = np.loadtxt("super_coffee_train.csv", delimiter=",", encoding='utf-8-sig')
testdata = np.loadtxt("super_coffee_test.csv", delimiter=",", encoding='utf-8-sig')
#x, y = traindata.shape
#print(traindata.shape)
x = 1000
y = 2

GAMMAR = 1.0
K = 0.5
global ii
ii = 1

m_TAU = 3.5 #3.5

m_datanum = 1000
m_datanum2 = 1
#m_datanum3 = 137

m_eps = 0.0
m_epsif = 0.0
m_fK = 0.5
m_btestmode = False

####
m_number = 1
m_number2 = 1
m_round = 1

num_onecluster = 0

#data = np.zeros(9)
fuzzy_member = np.zeros(20)
output_neuron = np.zeros(20)
cluster_centroid = np.zeros((1000, 40))
membership_value = 0.0
vigilance_constant = 0.0
vigilance_test_result = ''

data_read = np.zeros((9, 1000))
#old_cluster_centroid = np.zeros((9, 50))

m_cluster = 0

winner1c = 0
winner2c = 0

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

    global num_onecluster
    num_onecluster = 1

    global winner1c
    global winner2c
    if winner == 1:
        winner1c += 1
    elif winner == 2:
        winner2c += 1

def test_cluster():
    win_dist = np.zeros((y, 20))
    square_win_dist = np.zeros((y, 20))
    square_win_distance = np.zeros(20)
    de_win_distance = np.zeros(20)
    short_distance = 0.0
    exp_const = 0.0
    global membership_value
    global vigilance_constant
    global vigilance_test_result
    global cluster_centroid
    global winner
    global fuzzy_member

    for i in range(20):
        square_win_distance[i] = 0.0

    win_distance = np.zeros(20)

    #첫 번째 클러스터를 형성하고 두 번째 데이터가 들어오는 부분
    for i in range(1, m_cluster+1):
        #data[k] 현재 4차원 입력 데이터
        for k in range(m_datanum2):
            win_dist[k][i] = data[k] - cluster_centroid[k][i]
        for k in range(m_datanum2):
            square_win_dist[k][i] = win_dist[k][i]*win_dist[k][i]
        for k in range(m_datanum2):
            square_win_distance[i] += square_win_dist[k][i]
        win_distance[i] = np.double(square_win_distance[i])
        de_win_distance[i] = np.float(math.sqrt(win_distance[i]))

    #초기 winner = 1
    winner = 1
    short_distance = de_win_distance[1]

    #클러스터의 개수가 2개 이상일때, 클러스터간의 경쟁을 통하여 승자를 결정하고 vigilance test를 한다
    for i in range(2, m_cluster + 1):
        if short_distance > de_win_distance[i]:
            winner = i
            short_distance = de_win_distance[i]

    for i in range(1, m_cluster + 1):
        fuzzy_member[i] = 0.0

    #유클리디안 거리가 같을 때
    if short_distance == 0.0:
        fuzzy_member[winner] = 1.0
        membership_value = 1.0
    else:
        membership()

    #GAMMAR = 1
    #exp_const = float(-(GAMMAR*membership_value))
    #vigilance_constant = float(math.exp(exp_const))
    #vigilance_test()
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
        #print("uncommit실행")
        uncommit_cluster()

def membership():
    i = 0
    #distance = np.zeros((9, 10))
    #square_distance1 = np.zeros((9, 10))
    distance = np.zeros((4, 20))
    square_distance1 = np.zeros((4, 20))
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
    distance_winner1 = np.zeros(4)
    s_distance_winner = 0.0
    fuzzy_distance = 0.0
    distance_winner = 0.0
    temp = 0.0
    global vigilance_test_result
    global cluster_centroid

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
    winner_distance1 = np.zeros(4)
    s_winner_distance1 = np.zeros(4)
    s_winner_distance = 0.0
    function_iteration = 0.0
    pi_membership_td = 0.0
    pi_membership = np.zeros(20)

    distance = np.zeros((4, 20))
    square_distance1 = np.zeros((4, 20))
    square_distance = np.zeros(20)

    #update = 0.0
    #update_fuzzy = 0.0
    update = np.zeros(20)
    update_fuzzy = np.zeros(20)
    update_fuzzy_penalty = 0.0
    sqrt_distance = np.zeros(20)
    total_distance = 0.0

    data_average = np.zeros(4)
    average_centroid = np.zeros(4)
    data_av_com2 = 0.0
    data_av_distance = 0.0

    winner_distance = np.zeros(20)

    win_dist2 = np.zeros((4, 20))
    square_win_dist2 = np.zeros((4, 20))
    square_win_distance2 = np.zeros(20)
    de_win_distance2 = np.zeros(20)
    short_distance2 = 0.0

    win_distance2 = np.zeros(20)
    double_data_av_com2 = 0.0

    second_distance = np.zeros(20)
    short_distance3 = 0.0
    winner2 = 0
    winner3 = 0

    exponent = 0.0
    membership_relative = 0.0

    global cluster_centroid
    global output_neuron
    global num_onecluster
    num_onecluster += 1
    output_neuron[winner] = 1

    for i in range(1, m_cluster+1):
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

    #function_iteration = float(1.2 / (m_fK * m_number2))
    function_iteration = float(1.3/(m_fK*(m_number2 - 1) + 1))
    #1.3


    #############################################################
    #비지도학습과 다른 부분 시작
    #############################################################
    for i in range(1, m_cluster+1):
        square_win_distance2[i] = 0.0

    #첫 번째 클러스터를 형성하고 두 번째 데이터가 들어올 때
    for i in range(1, m_cluster+1):
        for k in range(m_datanum2):
            win_dist2[k][i] = data[k] - cluster_centroid[k][i]
        for k in range(m_datanum2):
            square_win_dist2[k][i] = win_dist2[k][i] * win_dist2[k][i]
            square_win_distance2[i] += square_win_dist2[k][i]

        win_distance2[i] = float(square_win_distance2[i])
        de_win_distance2[i] = float(math.sqrt(win_distance2[i]))

    #초기 winner2 = 1
    winner2 = 1
    short_distance2 = de_win_distance2[1]

    #클러스터의 개수가 2개 이상일때, 클러스터간의 경쟁을 통하여 승자를 결정하고 vigilance test를 한다
    for i in range(2, m_cluster + 1):
        if short_distance2 > de_win_distance2[i]:
            winner2 = i
            short_distance2 = de_win_distance2[i]

    for i in range(1, m_cluster + 1):
        second_distance[i] = de_win_distance2[i]

    ################################
    #second_distance[winner2] = de_win_distance2[1]
    second_distance[winner2] = 10000
    ################################

    winner3 = 1
    short_distance3 = second_distance[1]

    for i in range(2, m_cluster + 1):
        if short_distance3 > second_distance[i]:
            winner3 = i
            short_distance3 = second_distance[i]

    for i in range(10):
        square_distance[i] = 0.0

    total_distance = 0.0

    for i in range(1, m_cluster + 1):
        for k in range(m_datanum2):
            distance[k][i] = data[k] - cluster_centroid[k][i]
        for k in range(m_datanum2):
            square_distance1[k][i] = distance[k][i] * distance[k][i]
        for k in range(m_datanum2):
            square_distance[i] += square_distance1[k][i]
        sqrt_distance[i] = float(math.sqrt(float(square_distance[i])))
        total_distance += sqrt_distance[i]

    for k in range(m_datanum2):
        average_centroid[k] = 0.0

    for k in range(m_datanum2):
        average_centroid[k] = (cluster_centroid[k][winner2] + cluster_centroid[k][winner3]) / 2.0

    for k in range(m_datanum2):
        data_average[k] = data[k] - average_centroid[k]

    data_av_com2 = 0.0
    for k in range(m_datanum2):
        data_av_com2 = data_av_com2 + data_average[k] * data_average[k]

    double_data_av_com2 = float(data_av_com2)
    data_av_distance = float(math.sqrt(double_data_av_com2))

    exponent = -0.3 * data_av_distance #-3.9, -0.3

    membership_relative = float(math.exp(exponent))

    update_fuzzy = function_iteration * membership_value * membership_relative

    update_fuzzy_penalty = function_iteration * membership_value * membership_relative

    temp_cluster = np.zeros(9)

    global winner1c
    global winner2c
    if winner == 1:
        winner1c += 1
    elif winner == 2:
        winner2c += 1

    for a in range(4):
        temp_cluster[a] = 0.0

    if ii <= 500:
        if m_cluster == 1:
            for kk in range(1, num_onecluster + 1):
                temp_cluster[0] += data[0]

            temp_cluster[0] = float(temp_cluster[0] / num_onecluster)

            for k in range(m_datanum2):
                #print(cluster_centroid[k][1])
                cluster_centroid[k][1] = temp_cluster[k]
                #print(cluster_centroid[k][1])
        else:
            if winner == 1:
                for k in range(m_datanum2):
                    cluster_centroid[k][winner] = cluster_centroid[k][winner] + update_fuzzy * (data[k] - cluster_centroid[k][winner])
                    #print("winner1 :",winner ,cluster_centroid[k][winner])
            else:
                for k in range(m_datanum2):
                    cluster_centroid[k][winner] = cluster_centroid[k][winner] - update_fuzzy_penalty * (data[k] - cluster_centroid[k][winner])
                    #print("winner2 :",winner ,cluster_centroid[k][winner])

    elif ii > 500 and ii <= 1000:
        if m_cluster == 1:
            for kk in range(1, num_onecluster + 1):
                temp_cluster[0] += data[0]

            temp_cluster[0] = float(temp_cluster[0] / num_onecluster)

            for k in range(m_datanum2):
                cluster_centroid[k][1] = temp_cluster[k]
        else:
            if winner == 2:
                for k in range(m_datanum2):
                    cluster_centroid[k][winner] = cluster_centroid[k][winner] + update_fuzzy * (data[k] - cluster_centroid[k][winner])
                    #print("winner3 :",winner ,cluster_centroid[k][winner])
            else:
                for k in range(m_datanum2):
                    cluster_centroid[k][winner] = cluster_centroid[k][winner] - update_fuzzy_penalty * (data[k] - cluster_centroid[k][winner])
                    #print("winner4 :",winner ,cluster_centroid[k][winner])


    if num_onecluster == 1000:
        num_onecluster = 1

def uncommit_cluster():
    global m_cluster
    m_cluster = m_cluster + 1
    global output_neuron
    output_neuron[m_cluster] = 1
    global cluster_centroid

    for k in range(m_datanum2):
        #print(k, m_cluster)
        if m_cluster == 1:
            cluster_centroid[k][1] = cluster_centroid[k][1] - 0.5 * (data[k] - cluster_centroid[k][1])
            cluster_centroid[k][2] = data[k]
        else:
            cluster_centroid[k][m_cluster] = data[k]

    global winner1c
    global winner2c
    if winner == 1:
        winner1c += 1
    elif winner == 2:
        winner2c += 1

def learning():
    global data
    global ii
    global m_number2
    data = traindata[0:1] # x축은 0번째 요소, y축은 4개의 요소
    first_cluster()
    result = []
    ii += 1

    for i in range(1, x):
        data = traindata[i:i+1]
        test_cluster()
        ii += 1

    ii = 1
    m_number2 += 1

    count = 0
    epochs = 50
    error1 = 0
    error2 = 0

    for j in range(0, epochs): # 약 50번 수행 해야함
        for i in range(0, x):
            data = traindata[i:i+1]
            test_cluster()
            ii += 1
            if ii == 1000:
                ii = 1
            if j == epochs-1:
                count += 1
                if count == 1000:
                    count = 0
                if winner == 1:
                    if data >= 6:
                        error1 += 1
                elif winner == 2:
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

    for i in range(1, m_cluster+1):
        print(i, "번쨰 진하기 대표 값 :", end=" ")
        for j in range(m_datanum2):
            print(round(cluster_centroid[j][i]), end=" ")
            result.extend(str(int(round(cluster_centroid[j][i]))))

        print("")
    print("winner 1 error :", error1)
    print("winner 2 error :", error2)
    print("winner1 count :", winner1c)
    print("winner2 count :", winner2c)
    print("==============================================")

    # Start Test
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

    return result