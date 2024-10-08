package com.mentalhealth.project.system.posts.mapper;

import com.mentalhealth.project.system.posts.domain.Comment;
import com.mentalhealth.project.system.posts.domain.Posts;

import java.util.List;

/**
 * 帖子信息管理Mapper接口
 * 
 * @author wzxy
 * @date 2021-10-21
 */

public interface PostsMapper 
{
    /**
     * 查询帖子信息管理
     * 
     * @param postsId 帖子信息管理主键
     * @return 帖子信息管理
     */
    public Posts selectPostsByPostsId(Long postsId);

    /**
     * 查询帖子信息管理列表
     * 
     * @param posts 帖子信息管理
     * @return 帖子信息管理集合
     */
    public List<Posts> selectPostsList(Posts posts);

    /**
     * 前台查帖子列表
     * @return
     */
    public List<Posts> selectPostsWithPage(String postsTitle);

    /**
     * 新增帖子信息管理
     * 
     * @param posts 帖子信息管理
     * @return 结果
     */
    public int insertPosts(Posts posts);

    /**
     * 修改帖子信息管理
     * 
     * @param posts 帖子信息管理
     * @return 结果
     */
    public int updatePosts(Posts posts);

    /**
     * 删除帖子信息管理
     * 
     * @param postsId 帖子信息管理主键
     * @return 结果
     */
    public int deletePostsByPostsId(Long postsId);

    /**
     * 批量删除帖子信息管理
     * 
     * @param postsIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deletePostsByPostsIds(String[] postsIds);

    /**
     * 批量删除评论信息管理
     * 
     * @param postsIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteCommentByPostsIds(String[] postsIds);
    
    /**
     * 批量新增评论信息管理
     * 
     * @param commentList 评论信息管理列表
     * @return 结果
     */
    public int batchComment(List<Comment> commentList);
    

    /**
     * 通过帖子信息管理主键删除评论信息管理信息
     * 
     * @param postsId 帖子信息管理ID
     * @return 结果
     */
    public int deleteCommentByPostsId(Long postsId);

    /**
     * 查询评论总数
     * @param postsId
     * @return
     */
    public Long selectAllComment(Long postsId);


    /**
     * 根据所有帖子ID
     *
     * @return 帖子ID集合信息
     */
    public List<Posts> selectPostsAll();

    /**
     * 根据帖子ID查询帖子信息
     *
     * @param postsId 帖子ID
     * @return 帖子
     */
    public Posts selectPostsById(Long postsId);

    /**
     * 查询讨论数前十的帖子
     * @return
     */

    public List<Posts> getStatistic();


}
