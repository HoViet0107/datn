   M S B A M L   `   `   `  ����@  <AppUi, Version=1.0.0.0, Culture=neutral, PublicKeyToken=nullclr-namespace:AppUiAppUi  5   	       AppUi.MainWindow   5   	   W SPresentationCore, Version=8.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=8.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=8.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089R NWindowsBase, Version=8.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     5   	   R NSystem.Xaml, Version=8.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   %localclr-namespace:AppUi     5   	   -   5          �Name$
  main��5   	    � Title$ 
MainWindow��5   	   $	��600��6   $	��800��6)    � Cursor$ Arrow��65   .��5	      �  � ColumnDefinitions 5
   
   �� 5      $	��33* �6   �� 5      $
��167* �6   .+�5   
   �� $��2��6   .@�5      �� $��	Recommend��6   $��22��6)   $��
-2,-2,-2,0q�65   $	��Top=�6I   .��5      � ���	#FFE5E5E5.+�5      �� -   5         ��Name$ 	getRevBtn��5      $��	GetReview��60   $
��Left=�6D   $��	10,10,0,0q�6_   $	��Top=�6r   $��28��6�   $��63��6�    �� ContentStringFormat$ getReBtn��6�   4  .System.Windows.Automation.AutomationProperties   Name$ 	getRevBtn��6�   �� 5      -   5         ��Name$ csvList��5      $��
10,52,0,10q�6[   $
��Left=�6o   $	��147��6�   $��3��6�    J� RenderTransformOrigin$ 0.5,0.5&�6�   	 � ContextMenu	 5      �� 5      .@�5   "   m� -   5        $��Reload��5   +   6;   m� 5   "   -   5        $��Delete��5   +   6;   5      5      �� 5      -   5        $ 
predictBtn��5      $��Predict��61   $
��Left=�6C   $��	94,10,0,0q�6^   $	��Top=�6q   $��28��6�   $��63��6�   6�   &   System.Windows.Controls.DataGrid  5      -   5        
  Name$
 csvDF��5      $��174,52,10,10q�6Y   	 5      �� 5      .@�5   "   m� -   5        $��Clear��5   +   6:   5      5!      �� 5"      -	   5         ��Name$ prodUrl��5"      $
��Left=�6/   $��
174,10,0,0q�6J   $����https://tiki.vn/ao-thun-nam-co-be-vai-ca-sau-combo-2-ao-ez235-p22492292.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.239055_Y.1821375_Z.3709800_CN.Ao-thun-nam-co-be-vai-ca-sau%2C-Combo-2-ao-%E2%80%93-EZ235-21%2F04%2F2023&itm_medium=CPC&itm_source=tiki-ads&spid=22492294��6^   $	��Top=�6�  $	��493��6�  $��28��6�  $��15(�6�  �� 5#      $��Button��6   $
��Left=�6.   $��
700,10,0,0q�6I   $	��Top=�6]   $��28��6u   $��63��6�   5$      5%      �� 5&      $��CrawData��6   $��-2,-2,-19,0q�6(   .��5'      � ���	#FFE5E5E5.+�5(      �� $��Cateory��6   $
��Left=�6.   $��	30,15,0,0q�6I   $	��Top=�6\   �� 5)      -
   5         ��Name$ cateCbb��5)      $
��Left=�60   $��	96,16,0,0q�6K   $	��Top=�6^   $	��120��6v   $��27��6�   .@�5*      �� $��dien-tu-dien-lanh��6'   �� 5+      $��do-choi-me-be��6'   5,      �� 5-      -   5        $ crawlBtn��5-      $��Crawl��6/   $
��Left=�6?   $��
241,16,0,0q�6Z   $	��Top=�6n   $��54��6�   $��27��6�   6�   �� 5.      $��Train model��6   $��0,62,0,0q�64   	 5/      �� 50      .@�51   "   m� -   5        $��Train model��51   +   6@   52      54      �� 55      $��
Accuracy: ��6   $
��Left=�61   $��207,149,0,0q�6L   $	��Top=�6a   56      57      58      5:      5;      