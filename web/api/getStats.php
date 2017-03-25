<?php
    require("dbconnect.php");

    $videosScheduledCount = $mysqli->query("SELECT COUNT(*) From video");
    $videoCount = $mysqli->query("SELECT COUNT(*) From video Where NOT lastVisited IS NULL");
    $channelCount = $mysqli->query("SELECT COUNT(*) From channel");
    $commentCount = $mysqli->query("SELECT COUNT(*) From comment");

    echo json_encode([
        'channelCount' => $channelCount->fetch_all()[0][0],
        'videosScheduledCount' => $videosScheduledCount->fetch_all()[0][0],
        'videoCount' => $videoCount->fetch_all()[0][0],
        'commentCount' => $commentCount->fetch_all()[0][0]
    ]);
?>