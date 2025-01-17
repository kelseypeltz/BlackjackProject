import random
class Strategy:

    def RandomAction(self):
        if random.random() <= 0.5:
            return 0
        elif random.random() <= 0.75:
            return 1
        elif random.random() <= 0.9:
            return 2
        else:
            return 3
    def EpsilonGreedyPolicyFromQTableDict(self, epsilon, QTableDict, playerCardPoints, dealerCardPoints, playerCardUsableAce):
        # P = epsilon: exploration
        if random.random() < epsilon:
            return self.RandomAction()
        # P = 1-epsilon: exploitation
        else:
            return self.BestActionPolicyFromQTableDict(QTableDict, playerCardPoints, dealerCardPoints, playerCardUsableAce)

    def BestActionPolicyFromQTableDict(self, QTableDict, playerCardPoints, dealerCardPoints, playerCardUsableAce):
        # Q function for state (playerCardPoints, dealerCardPoints, hit)
        hitValue = QTableDict[(playerCardPoints, dealerCardPoints, playerCardUsableAce, 0)]
        # Q function for state (playerCardPoints, dealerCardPoints, stick)
        stickValue = QTableDict[(playerCardPoints, dealerCardPoints, playerCardUsableAce, 1)]
        # Q function for state (playerCardPoints, dealerCardPoints, double)
        doubleValue = QTableDict[(playerCardPoints, dealerCardPoints, playerCardUsableAce, 2)]
        # Q function for state (playerCardPoints, dealerCardPoints, split)
        splitValue = QTableDict[(playerCardPoints, dealerCardPoints, playerCardUsableAce, 3)]

        if splitValue > hitValue and splitValue > stickValue and splitValue > doubleValue:
            return 3
        elif doubleValue > hitValue and doubleValue > stickValue:
            return 2
        elif hitValue > stickValue:
            return 0
        elif stickValue > hitValue:
            return 1
        else:
            return self.RandomAction()

    def UpdateQTableDict(self, reward, occurredStateActions, QTableDict, stateCount, stateActionCount, method, gamma = 0.8):
        # update over all keys
        for i in range(len(occurredStateActions)):
            state = occurredStateActions[i][:-1]
            stateAction = occurredStateActions[i]
            # update counts
            stateCount[state] += 1
            stateActionCount[stateAction] += 1

            # set the learning rate
            alpha = 1.0 / stateActionCount[stateAction]

            # update value function
            # for Q-learning or Sarsa
            if (method == "Q-Learning" or method == "Sarsa"):
                previousQ = QTableDict[stateAction]
                # calculate the best Q value for (next state, best action)
                if i < len(occurredStateActions) - 1:
                    # for Q-learning
                    if (method == "Q-Learning"):
                        nextStateHitAction = occurredStateActions[i + 1][:-1] + (0,)
                        nextStateStickAction = occurredStateActions[i + 1][:-1] + (1,)
                        nextStateDoubleAction = occurredStateActions[i + 1][:-1] + (2,)
                        nextStateSplitAction = occurredStateActions[i + 1][:-1] + (3,)
                        maxvalue = max(QTableDict[nextStateHitAction], QTableDict[nextStateStickAction], QTableDict[nextStateDoubleAction], QTableDict[nextStateSplitAction])
                        bestNextQ = gamma * maxvalue
                    # for Sarsa
                    else:
                        nextStateAction = occurredStateActions[i + 1]
                        bestNextQ = gamma * QTableDict[nextStateAction]
                else:
                    bestNextQ = 0

                # update the Q table dict
                QTableDict[occurredStateActions[i]] = (1 - alpha) * previousQ + alpha * (reward + bestNextQ)

            # for Temporal Difference
            else:
                QTableDict[occurredStateActions[i]] += alpha * (reward - QTableDict[occurredStateActions[i]])
                

