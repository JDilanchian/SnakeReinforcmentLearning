import torch
import torch.nn as nn
import torch.optim as optim 
import torch.nn.functional as F
import os 

class Linear_Qnet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, file_name='model.pth'):
        mdoel_folder_path = './model'
        if not os.path.exists(mdoel_folder_path):
            os.makedirs(mdoel_folder_path)
        
        file_name = os.path.join(mdoel_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer: 
    def __init__(self, model, lr, gamma) -> None:
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.lr) # pytorch optimization step 
        
        self.criterion = nn.MSELoss() # loss function
    
    #state_old, final_move, reward, state_new, done
    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype = torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # we dont need this of the "done"

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0) # axis 0 which addes a dimention to the begning 
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            state = torch.unsqueeze(state, 0)
            done = (done, )

        # 1: predicted Q values with current state 
        pred = self.model(state) # -> this is "action" which has 3 parameters 
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action).item()] = Q_new
        # 2: Q_new = r + y * max(next_predicted Q value) -> only one value (we do this when not done)
        # pred.clone()
        # preds[argmax(action)] = Q_new 
        
        self.optimizer.zero_grad() # to empty the gradient 
        loss = self.criterion(target, pred)
        loss.backward()
        
        self.optimizer.step()


